import os
import cv2
import numpy as np
import face_recognition
import threading
import mediapipe as mp
from django.utils import timezone
from datetime import datetime, time 
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from attendance.models import Attendance
from employees.models import Employee
from collections import defaultdict
from datetime import datetime, timedelta,date
 



# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

KNOWN_FACES, KNOWN_NAMES = [], []
DETECTION_RESULTS = {
    'name':[],
}

face_lock = threading.Lock()





def load_known_faces():
    """Load and encode known faces from media directory."""
    media_dir = settings.MEDIA_ROOT
    if not os.path.exists(media_dir):
        print("⚠ Media directory not found!")
        return
    global KNOWN_FACES, KNOWN_NAMES
    with face_lock:
        KNOWN_FACES.clear()
        KNOWN_NAMES.clear()
        
        image_extensions = ('.jpg', '.jpeg', '.png')
        media_files = [f for f in os.listdir(media_dir) if f.lower().endswith(image_extensions)]
        
        for filename in media_files:
            path = os.path.join(media_dir, filename)
            
            try:
                img = face_recognition.load_image_file(path)
                encodings = face_recognition.face_encodings(img, num_jitters=1, model='hog')
                
                if encodings:
                    KNOWN_FACES.append(encodings[0])
                    KNOWN_NAMES.append(os.path.splitext(filename)[0].replace('_', ' '))
                    print(f"✔ Loaded: {filename}")
                else:
                    print(f"⚠ No face detected in {filename}")
            except Exception as e:
                print(f"⚠ Error loading {filename}: {e}")
                

def get_camera_frame(cap):
    """Capture a frame from the camera."""
    success, frame = cap.read()
    return frame if success else None

def process_frame(frame, face_detector):
    global DETECTION_RESULTS
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detector.process(rgb_frame)

    detected_names = []
    if results.detections:
        frame_height, frame_width = frame.shape[:2]

        face_locations = []
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            top = int(max(0, bbox.ymin * frame_height))
            left = int(max(0, bbox.xmin * frame_width))
            bottom = int(min(frame_height, (bbox.ymin + bbox.height) * frame_height))
            right = int(min(frame_width, (bbox.xmin + bbox.width) * frame_width))
            
            face_locations.append((top, right, bottom, left))

        encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for (top, right, bottom, left), encoding in zip(face_locations, encodings):
            name = "Unknown"
            if KNOWN_FACES:
                face_distances = face_recognition.face_distance(KNOWN_FACES, encoding)
                best_match_index = np.argmin(face_distances)

                if face_distances[best_match_index] < 0.6:
                    name = KNOWN_NAMES[best_match_index]

            detected_names.append(name)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            
    DETECTION_RESULTS = {"name": detected_names}
    return frame, detected_names

def video_stream():
    """Stream live video with face detection."""
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as detector:
        while True:
            frame = get_camera_frame(cap)
            if frame is None:
                continue
            
            processed_frame, detected_names = process_frame(frame, detector)
            _, buffer = cv2.imencode('.jpg', processed_frame)
           

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def video_feed(request):
    """Return streaming response for video feed."""
    return StreamingHttpResponse(video_stream(), content_type='multipart/x-mixed-replace; boundary=frame')

def get_employee_data(request):
    """Return detected employee names"""
    global DETECTION_RESULTS
    return JsonResponse({
        'ids': DETECTION_RESULTS.get("id", []),
        "names": DETECTION_RESULTS.get("name", []),
        "fresh": True  # Add this flag to avoid undefined errors in JavaScript
    })

    

@login_required
def mark_attendance(request):
    """Render attendance page with preloaded known faces."""
    load_known_faces()
    return render(request, 'mark_attendance.html', {
        "employees": Employee.objects.all(),
        "attendance_types": ["Check In", "Check Out", "Break In", "Break Out", "For Market", "From Market", "For Vendor", "From Vendor"],
    })

def save_attendance(request):
    """Save attendance record if employee exists."""
    if request.method == "POST":
        name = request.POST.get("employee_name")
        att_type = request.POST.get("attendance_type")
        
        if not name or not att_type:
            messages.error(request, "Please select an employee and attendance type.")
            return redirct('attendance:mark_attendance')
        
        try:
            employee= Employee.objects.get(name=name)
        except Employee.DoesNotExist:
            messages.error(request, "Employee Not Found") 
            return redirct('attendance:mark_attendance')
        
        now = timezone.now()
        today = now.date()
        late_minutes = 0
        
        if att_type == "Check In":
            already_checked_in = Attendance.objects.filter(
                employee=employee,
                attendance_type="Check In",
                date=today
            ).exists()
            
            if already_checked_in:
                messages.error(request, f"{employee.name} already Checked In Today")
                return redirect('attendance:mark_attendance')
            
            # late minutes logic
            expected_time = time(8,0,0)
            expected_datetime = timezone.make_aware(datetime.combine(today, expected_time))
            
            if now > expected_datetime:
                late_delta = now-expected_datetime
                late_minutes = int(late_delta.total_seconds() // 60)
                print(f"Late minutes for {employee.name}: {late_minutes} min")
                
                
            # record check in  
            Attendance.objects.create(
                employee=employee,
                attendance_type = att_type,
                late_minutes = late_minutes,
                status="Present",
                timestamp=now,
                date=today
            )
            
            employee.status = "Present"
            employee.save()
            return redirect('attendance:attendance_list')
        elif att_type == "Check Out":
            already_checked_out = Attendance.objects.filter(
                employee=employee,
                attendance_type="Check Out",
                date=today
            ).exists()
            
            if already_checked_out:
                messages.error(request, f"{employee.name} already checked out in today")
                return redirect('attendance:mark_attendance')
            
            # check if employee has check in today or not 
            
            check_in_exists = Attendance.objects.filter(
                employee=employee,
                attendance_type='Check In',
                date=today
            ).exists()
            
            if not check_in_exists:
                messages.error(request, f"{employee.name} has not checked in today yet ")
                return redirect('attendance:mark_attenance')
            
            Attendance.objects.create(
                employee=employee,
                attendance_type=att_type,
                timestamp=now,
                date=today
            )
            
            employee.status = "Leave"
            employee.save()
            
            return redirect('attendance:attendance_list')
        
        elif att_type in ["Break In", "Break Out", "For Market", "From Market", "For Vendor", "From Vendor"]:
            Attendance.objects.create(
                employee=employee,
                attendance_type=att_type,
                timestamp=now,
                date=today
            )
            
            return redirect('attendance:attendance_list')
        else:
            messages.error(request,"Invalid  Attendance Type")
        
    messages.error(request, "Invalid Request Type")
            
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    #     employee = Employee.objects.get(name=name)
    #     now = timezone.now()
    #     today = now.date()
    #     late_minutes = 0
        
    #     already_checked_in = Attendance.objects.filter(employee=employee, attendance_type="Check In", date=today).exists()
    #     if already_checked_in:
    #         try:
    #             if att_type == "Check In" and employee.status == "active":
    #                 expected_time = time(8, 0,0)
    #                 expected_datetime = timezone.make_aware(datetime.combine(today, expected_time))
                    
    #                 if now > expected_datetime:
    #                     late_delta = now - expected_datetime
    #                     late_minutes = int(late_delta.total_seconds() // 60)
    #                     print(f"Late minutes for {employee.name}: {late_minutes} min")
                    
    #             Attendance.objects.create(
    #                 employee=employee, 
    #                 attendance_type=att_type, 
    #                 timestamp=now, 
    #                 late_minutes=late_minutes,
    #                 status="Present",
    #                 date=today
    #                 )
    #             return redirect('attendance:attendance_list')
    #         except Employee.DoesNotExist:
    #             return JsonResponse({"error": "Employee not found"}, status=404)
    #     return redirect('attendance:mark_attendance')

    # return JsonResponse({"error": "Invalid request"}, status=400)





def get_daily_summary(request, date=None):
    today = datetime.today().date() if date is None else date
    records_data = Attendance.objects.filter(timestamp__date=today).order_by('employee', 'timestamp')
    
    records = [Attendance.objects.get(pk=r.pk) for r in records_data if r.timestamp.date() == today]
    records.sort(key=lambda r: (r.employee.name, r.timestamp))

    attendance_data = []
    # Use a dictionary to track processed employees to avoid duplicates
    processed_employees = {}
    employee_late_minutes = {}
    
    # print late minutes
    for r in records:
        print(f"Attendance Record: {r.employee.name} - {r.attendance_type} - {r.late_minutes} Minutes")
        
    for record in records:
        if record.attendance_type == "Check In":
            late_minutes = record.late_minutes
            is_late = record.is_late()
            print(f"Late minutes for {record.employee.name}: {late_minutes} min")
            employee_late_minutes[record.employee.id] = late_minutes
    
    print("Employee Late Minutes: ", employee_late_minutes)
    
    for employee in {r.employee for r in records}:  # Using set to get unique employees
        if employee.id in processed_employees:
            continue  # Skip if already processed
            
        processed_employees[employee.id] = True  # Mark as processed
        emp_records = [r for r in records if r.employee == employee]

        # Get first check-in and last check-out
        check_ins = [r.timestamp for r in emp_records if r.attendance_type == "Check In"]
        check_outs = [r.timestamp for r in emp_records if r.attendance_type == "Check Out"]
        
        check_in = check_ins[0] if check_ins else None
        check_out = check_outs[-1] if check_outs else None
        status = "✅ Present" if check_in else "❌ Absent"

        late_minutes = employee_late_minutes.get(employee.id, 0)
        is_late = late_minutes > 0
        break_minutes = 0
        market_minutes = 0
        vendor_minutes = 0
        work_minutes = None
        work_display = "N/A"
        late_display = "🟢 No"
        overtime_display = ""

        i = 0
        while i < len(emp_records):
            r = emp_records[i]
            if r.attendance_type == "Break Out" and i + 1 < len(emp_records) and emp_records[i + 1].attendance_type == "Break In":
                duration = emp_records[i + 1].timestamp - r.timestamp
                break_minutes += int(duration.total_seconds() / 60)
                i += 1

            elif r.attendance_type == "For Market" and i + 1 < len(emp_records) and emp_records[i + 1].attendance_type == "From Market":
                duration = emp_records[i + 1].timestamp - r.timestamp
                market_minutes += int(duration.total_seconds() / 60)
                i += 1

            elif r.attendance_type == "For Vendor" and i + 1 < len(emp_records) and emp_records[i + 1].attendance_type == "From Vendor":
                duration = emp_records[i + 1].timestamp - r.timestamp
                vendor_minutes += int(duration.total_seconds() / 60)
                i += 1
            i += 1

        # Late Display Logic
        if late_minutes > 0:
            if late_minutes < 60:
                late_display = f"{late_minutes} min"
            else:
                late_display = f"{late_minutes // 60}h {late_minutes % 60}m"
        else:
            late_display = "🟢 No"
        
        if check_in and check_out:
            total_duration = check_out - check_in
            total_minutes = int(total_duration.total_seconds() / 60)
            work_minutes = total_minutes - break_minutes
            work_display = f"{work_minutes // 60}h {work_minutes % 60}m"
            # Overtime logic (example: work time above 8 hours)
            if work_minutes > 480:
                ot = work_minutes - 480
                overtime_display = f"{ot // 60}h {ot % 60}m"
        elif check_in and not check_out:
            work_display = "🟡 Still Working"
            
        is_late_flag = late_minutes > 0
        print(f"{employee.name} - Late Minutes: {late_minutes} - Is Late: {is_late_flag}")
        
        attendance_data.append({
            'employee': employee,
            'check_in': check_in,
            'check_out': check_out,
            'status': status,
            'late_display': late_display,
            'late_minutes': late_minutes,
            'work_display': work_display,
            'overtime_display': overtime_display,
        })

    return render(request, "attendance_list.html", {
        'attendance_data': attendance_data,
    })

def calculate_monthly_payroll(employee, month, year):
    # Get all attendance records for the employee for the given month and year
    first_day = datetime(year, month, 1).date()
    last_day = (datetime(year, month + 1, 1) - timedelta(days=1)).date()

    total_work_minutes = 0
    total_late_minutes = 0
    total_break_minutes = 0
    total_market_minutes = 0
    total_vendor_minutes = 0

    # Check if employee status is active
    if employee.status == "active":
        for day in range((last_day - first_day).days + 1):
            date = first_day + timedelta(days=day)
            summary = get_daily_summary(employee, date)
            
            total_work_minutes += summary['work_minutes']
            total_late_minutes += summary['late_minutes']
            total_break_minutes += summary['break_minutes']
            total_market_minutes += summary['market_minutes']
            total_vendor_minutes += summary['vendor_minutes']

        # Example: Calculate monthly salary based on work minutes, deducting for late, etc.
        hourly_rate = 10  # Define your hourly rate
        salary = (total_work_minutes / 60) * hourly_rate

        # Deduct for late minutes if necessary
        late_deduction = total_late_minutes * 0.1  # Deduct 0.1 for each late minute
        salary -= late_deduction

        return {
            'total_work_minutes': total_work_minutes,
            'total_late_minutes': total_late_minutes,
            'salary': salary,
        }
    else:
        return {
            'total_work_minutes': 0,
            'total_late_minutes': 0,
            'salary': 0,
        }


def employee_detailed_attendance(request, employee_id=None):
    """Render grouped attendance list page, or details of a specific employee."""
    
    if employee_id:
        # Get attendance only for the selected employee
        employee = get_object_or_404(Employee, id=employee_id)
        attendance_records = Attendance.objects.filter(employee=employee).order_by("timestamp")
    else:
        # Get attendance for all employees
        attendance_records = Attendance.objects.all().order_by("employee", "timestamp")

    grouped_attendance = defaultdict(lambda: {
        "check_in": None, "check_out": None, 
        "market_time": timedelta(), "vendor_time": timedelta(),
        "break_time": timedelta()
    })

    for record in attendance_records:
        key = (record.employee, record.timestamp.date())

        if record.attendance_type == "Check In" and not grouped_attendance[key]["check_in"]:
            grouped_attendance[key]["check_in"] = record.timestamp

        elif record.attendance_type == "Check Out":
            grouped_attendance[key]["check_out"] = record.timestamp

        elif record.attendance_type == "For Market":
            grouped_attendance[key]["market_start"] = record.timestamp

        elif record.attendance_type == "From Market" and "market_start" in grouped_attendance[key]:
            grouped_attendance[key]["market_time"] += record.timestamp - grouped_attendance[key]["market_start"]
            del grouped_attendance[key]["market_start"]

        elif record.attendance_type == "For Vendor":
            grouped_attendance[key]["vendor_start"] = record.timestamp

        elif record.attendance_type == "From Vendor" and "vendor_start" in grouped_attendance[key]:
            grouped_attendance[key]["vendor_time"] += record.timestamp - grouped_attendance[key]["vendor_start"]
            del grouped_attendance[key]["vendor_start"]

        elif record.attendance_type == "Break Out":
            grouped_attendance[key]["break_start"] = record.timestamp

        elif record.attendance_type == "Break In" and "break_start" in grouped_attendance[key]:
            grouped_attendance[key]["break_time"] += record.timestamp - grouped_attendance[key]["break_start"]
            del grouped_attendance[key]["break_start"]

    # Prepare data for the template
    attendance_data = []
    today = datetime.now().date()
    expected_check_in = datetime.strptime("09:00", "%H:%M").time()

    for (employee, date), times in grouped_attendance.items():
        check_in_time = times["check_in"]
        check_out_time = times["check_out"]
        market_time = times["market_time"]
        vendor_time = times["vendor_time"]
        break_time = times["break_time"]

        # ✅ Late Calculation
        late_minutes = None
        if check_in_time and check_in_time.time() > expected_check_in:
            late_minutes = (datetime.combine(date, check_in_time.time()) - datetime.combine(date, expected_check_in)).seconds // 60

        # ✅ Calculate Total Working Hours (Check-out - Check-in) minus break time
        working_hours = None
        if check_in_time and check_out_time:
            total_time = check_out_time - check_in_time
            net_working_time = total_time - break_time
            working_hours = f"{net_working_time.seconds // 3600}h {((net_working_time.seconds // 60) % 60)}m"

        attendance_data.append({
            "employee": employee,
            "employee_id": employee.id,
            "date": date,
            "check_in": check_in_time.strftime("%I:%M %p") if check_in_time else "-",
            "check_out": check_out_time.strftime("%I:%M %p") if check_out_time else "-",
            "market_hours": f"{market_time.seconds // 3600}h {((market_time.seconds // 60) % 60)}m" if market_time else "-",
            "vendor_hours": f"{vendor_time.seconds // 3600}h {((vendor_time.seconds // 60) % 60)}m" if vendor_time else "-",
            "break_hours": f"{break_time.seconds // 3600}h {((break_time.seconds // 60) % 60)}m" if break_time else "-",
            "status": "✅ Present" if check_in_time and check_out_time else "❌ Absent",
            "late": f"{late_minutes} min ⚠️" if late_minutes else "🟢 No",
            "working_hours": working_hours if working_hours else "-",
        })

    if employee_id:
        # Show only today's record and history for the month
        employee_attendance = [entry for entry in attendance_data if entry["employee"].id == employee_id]
        today_attendance = [entry for entry in employee_attendance if entry["date"] == today]
        monthly_attendance = employee_attendance

        return render(request, "employee_attendance_detail.html", {
            "employee": employee,
            "today_attendance": today_attendance,
            "monthly_attendance": monthly_attendance,
        })
    print(attendance_data)

    return render(request, "attendance_list.html", {"attendance_data": attendance_data})


# delete daily attendance record if need
def delete_attendance(request, attendance_id):
    """ Delete an Attendance record by ID """
    try:
        if request.method == "POST":
            attendance = get_object_or_404(Attendance, id=attendance_id)
            attendance.delete()
            return redirect('attendance:attendance_list')
        return redirect('attendance:attendance_list')
    except Attendance.DoesNotExist:
        return JsonResponse({"error": "Attendance record not found"}, status=404)
    