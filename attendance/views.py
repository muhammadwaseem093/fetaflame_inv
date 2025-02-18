from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AttendanceForm
from .models import Attendance
from django.contrib import messages
from django.utils import timezone
from employees.models import Employee
from django.utils.timezone import datetime

def mark_attendance(request):
    employees = Employee.objects.all()
    
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        status = request.POST.get('status')
        employee = Employee.objects.get(id=employee_id)
        
        attendance = Attendance.objects.create(
            employee=employee,
            status=status,
            attendance_date=datetime.today().date(),
        )
        if status == 'Late':
            late = Attendance.is_late(attendance)
            if late:
                messages.warning(request, 'You are late today!')
        
        return redirect('attendance_report') 
    
    return render(request, 'mark_attendance.html', {'employees': employees})

def attendance_report(request):
    today = datetime.today().date()
    employees = Employee.objects.all()
    for employee in employees:
        attendance_today = employee.attendance_set.filter(attendance_date=today).first()
        employee.attendance_today = attendance_today
    
    return render(request, 'attendance_list.html', {'employees': employees, 'today': today})




