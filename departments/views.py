from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from utils.decorators import role_required
from django.contrib import messages
from .models import Department
from .forms import DepartmentForm


@login_required
@role_required('hr', 'admin')
def create_dept(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department Created Successfull!')
            return redirect('view_dept')
        else:
            messages.error(request, 'Department Creation Failed')
    else:
        form = DepartmentForm()
    return render(request, 'create_department.html', {'form':form})

@login_required
@role_required('hr', 'admin')
def view_dept(request):
    department = Department.objects.all()
    return render(request, 'department_list.html', {'department':department})  

@login_required
@role_required('staff','hr','admin')
def update_dept(request, pk):
    department = Department.objects.get(id=pk)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department Update Successfully!')
            return redirect('view_dept')
        else:
            messages.error(request, 'Department Creation Failed')
            return render(request, 'edit_department.html', department_id)
    else:
        form = DepartmentForm()
    return render(request, 'edit_department.html', {"form":form, "department":department})


@login_required
@role_required('admin')
def delete_dept(request, pk):
    try:
        department = Department.objects.get(id=pk)
    except Unit.DoesNotExist:
        raise Http('Department Not Found')
    
    if request.method == 'POST':
        department.delete()
        messages.success(request, "Department Deleted Successfully!")
        return redirect('view_dept')
    return render(request, 'delete_dept.html', {'department':department})