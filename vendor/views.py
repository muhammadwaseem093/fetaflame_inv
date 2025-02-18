from django.shortcuts import render,redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages 
from utils.decorators import role_required
from django.contrib.auth.decorators import login_required
from .models import Vendor
from .forms import VendorForm
from utils.helpers import search_and_paginate


@login_required
@role_required('staff', 'hr', 'admin')
def vendor_list(request):
    filters = {
        'name': 'name',
    }
    
    vendor_list, search_params = search_and_paginate(
        request,
        model=Vendor,
        filters=filters,
        ordering='name',
        per_page=10,
    )
    
    return render(request, 'vendor_list.html', {
        'vendor_list': vendor_list,
        'search_params': search_params,
        'search_active': bool(search_params),
    })

@login_required
@role_required('staff', 'hr', 'admin')
def create_vendor(request):
    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendor Created Successfully!')
            return redirect("vendor_list")
        else:
            messages.error(request, 'Vendor Creation Failed')
    else:
        form = VendorForm()
    return render(request, 'create_vendor.html', {"form":form})

@login_required
@role_required('staff', 'hr', 'admin')
def update_vendor(request, pk):
    vendor = Vendor.objects.get(id=pk)
    if request.method =="POST":
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, "Vendor Updated Successfully!")
            return redirect("vendor_list")
        else:
            messages.error(request, "Vendnor Updation Failed")
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'edit_vendor.html', {"form":form, "vendor":vendor})

@login_required
@role_required('hr','admin')
def delete_vendor(request, pk):
    try:
        vendor = Vendor.objects.get(id=pk)
    except Vendor.DoesNotExist:
        raise Http404('Vendors Does Not Exist')
    
    if request.method == "POST":
        vendor.delete()
        messages.success(request, "Vendor Deleted Successfully!")
        return redirect("vendor_list")
    return render(request, 'delete_vendor.html', {"vendor":vendor})