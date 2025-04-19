from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from .forms import UnitForm
from .models import Unit
from django.contrib.auth.decorators import login_required
from utils.decorators import role_required


@login_required
@role_required('staff','hr','admin')
def unit_list(request):
    units = Unit.objects.all()
    return render(request, 'unit_list.html', {"units":units})


@login_required
@role_required('staff','hr','admin')
def create_unit(request):
    if request.method == "POST":
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Unit Created Successfully!")
            return redirect('units:unit_list')
        else:
            messages.error(request, "Unit Creation Failed")
    else:
        form = UnitForm()
    return render(request, 'create_unit.html', {"form":form})


@login_required
@role_required('admin')
def update_unit(request, pk):
    unit = Unit.objects.get(id=pk)
    if request.method == "POST":
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unit Updated Successfully!')
            return redirect('units:unit_list')
        else:
            messages.error(request, "Unit Update Failed")
    else:
        form = UnitForm(instance=unit)
    return render(request, 'edit_unit.html', {"form":form, "unit":unit})


@login_required
@role_required('admin')
def delete_unit(request, pk):
    try:
        unit = Unit.objects.get(id=pk)
    except Unit.DoesNotExist:
        raise Http404('Unit Does Not Exist!')
    if request.method == 'POST':
        unit.delete()
        messages.success(request, 'Unit Deleted Successfully!')
        return redirect('units:unit_list')
    return render(request, 'delete_unit.html', {"unit":unit})

def error_page(request):
    return render(request, 'error.html')