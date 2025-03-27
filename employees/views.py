from django.shortcuts import render,redirect,get_object_or_404
import numpy as np
import face_recognition
import json
import cv2
from PIL import Image
import io
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utils.decorators import role_required
from django.http import Http404
from .models import Employee
from departments.models import Department
from .forms import EmployeeForm
from utils.helpers import search_and_paginate
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
# face detection related lib
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.http import JsonResponse


def encode_face(image_path):
    try:
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        print(f"Image Shape : {img.shape}- {image_path}- {type(img)}- {img}")
        if img is None:
            print("Error: Image Not Loaded Properly!")
            return None 
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        print(f"Image Shape : {img_rgb.shape}")
        
        print(f"Image Shape : {img_rgb.shape}")     
        print(f"Image Data Type:{img_rgb.dtype}")  
        print(f"Image Mode is : {pil_image.mode}") 
        face_encodings = face_recognition.face_encodings(img_rgb)
        print(f"Face Encodings: {face_encodings}")
        
        if len(face_encodings) > 0:
            return face_encodings[0]
        else:
            print("Error: No Face Detected.")
            return None 
        
    except Exception as e:
        print(f"Error Processing Image: {e}")
        return None 
        










@login_required
@role_required('staff','hr','admin')
def employee_list(request):
    filters = {
        "name":'name',
    }
    
    employee_list, search_params = search_and_paginate(
        request,
        model=Employee,
        filters=filters,
        ordering='id',
        per_page=10,
    )
    
    return render(request, 'employee_list.html', {
        'employee_list':employee_list,
        'search_params':search_params,
        'search_active': bool(search_params),
    })

@login_required
@role_required('hr','admin')
def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
            if employee.photo:
                employee.photo.name = employee.photo.name.replace(" ","_")
                employee.save()
                image_path = os.path.join(settings.MEDIA_ROOT, str(employee.photo))
                print(image_path)
                face_encoding = encode_face(image_path)
                print(face_encoding)
                if face_encoding is not None:
                    employee.face_encoding = json.dumps(face_encoding.tolist())
                    employee.save()
                    print(employee.face_encoding)
                else:
                    messages.error(request, "Face Encoding Failed")
            messages.success(request, "Employee Created Successfully")
            return redirect('employees:employee_list')
    else:
        form = EmployeeForm()
    
    departments = Department.objects.all()
    return render(request, 'create_employee.html', {
        'form': form,
        'departments': departments
    })
    
    
@login_required
@role_required('hr','admin')
def update_employee(request,pk):
    employees = get_object_or_404(Employee, pk=pk)
    departments = Department.objects.all()
    
    if request.method == "POST":
        department_id = request.POST.get('department')
        if department_id and department_id.isdigit():
            try:
                employees.department = Department.objects.get(pk=int(department_id))
            except Department.DoesNotExist:
                messages.error(request, "Selected Department does not exist")
                return redirect('employees:employee_list', pk=pk)
            
        form = EmployeeForm(request.POST, instance=employees)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee Updated  Successfully!")
            return redirect('employees:employee_list')
        else:
            messages.error(request, 'Employee Update Failed!')
    else:
        form = EmployeeForm(instance=employees)
    return render(request, 'employee_edit.html', {"form":form, "employees":employees, "departments":departments})


@login_required
@role_required('hr','admin')
def delete_employee(request, pk):
    try:
        employee = Employee.objects.get(id=pk)
    except Employee.DoesNotExist:
        raise Http404('Employee Not Exist')
    
    if request.method == "POST":
        employee.delete()
        messages.success(request, "Employee Deleted Successfully")
        return redirect("employees:employee_list")
    return render(request, 'delete_employee.html', {"employee":employee})


def error_page(request):
    return render(request, 'error.html')
