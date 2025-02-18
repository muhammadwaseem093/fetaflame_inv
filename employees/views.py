from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utils.decorators import role_required
from django.http import Http404
from .models import Employee
from departments.models import Department
from .forms import EmployeeForm
from utils.helpers import search_and_paginate

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
            form.save()
            return redirect('employees:employee_list')  # Redirect to employee list
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
    employees = Employee.objects.get(id=pk)
    departments = Department.objects.all()
    
    if request.method == "POST":
        department_id = request.POST.get('department')
        try:
            employees.department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            messages.error(request, "Selected Supplier does not exist")
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
