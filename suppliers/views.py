from django.shortcuts import render,redirect 
from django.contrib import messages 
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from utils.decorators import role_required
from .models import Supplier
from .forms import SupplierForm
from utils.helpers import search_and_paginate


@login_required
@role_required('hr','admin','staff')
def supplier_list(request):
    filters = {
        'name': 'name',
    }
    supplier_list, search_params = search_and_paginate(
        request,
        model=Supplier,
        filters=filters,
        ordering='name',
        per_page=10,
    )
    return render(request, 'supplier_list.html', {
        'supplier_list': supplier_list,
        'search_params': search_params,
        'search_active': bool(search_params),
    })


@login_required
@role_required('hr','admin','staff')
def create_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier Created Successfully!')
            return redirect(reverse('suppliers:supplier_list'))
        else:
            messages.error(request, 'Supplier Creation Failed')
    else:
        form = SupplierForm()
    return render(request, 'create_supplier.html',{'form':form})


@login_required
@role_required('hr','staff','admin')
def update_supplier(request, pk):
    supplier = Supplier.objects.get(id=pk)
    if request.method =="POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request,'Supplier Updated Successfully!')
            return redirect(reverse('suppliers:supplier_list'))
        else:
            messages.error(request, 'Supplier Update Failed')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'supplier_edit.html', {"form":form,"supplier":supplier})


@login_required
@role_required('hr','admin')
def delete_supplier(request, pk):
    try:
        supplier = Supplier.objects.get(id=pk)
    except Supplier.DoesNotExist:
        raise Http404('Supplier Does Not Exisr')
    
    if request.method == "POST":
        supplier.delete()
        messages.success(request, 'Supplier Deleted Successfully!')
        return redirect(reverse('suppliers:supplier_list'))
    return render(request, 'delete_supplier.html', {'supplier':supplier})

def error_page(request):
    return render(request, 'error.html')