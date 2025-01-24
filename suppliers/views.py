from django.shortcuts import render,redirect 
from django.contrib import messages 
from django.http import Http404
from django.contrib.auth.decorators import login_required
from utils.decorators import role_required
from .models import Supplier
from .forms import SupplierForm


@login_required
@role_required('hr','admin','staff')
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers':suppliers})


@login_required
@role_required('hr','admin','staff')
def create_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier Created Successfully!')
            return redirect('supplier_list')
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
            return redirect("supplier_list")
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
        return redirect('supplier_list')
    return render(request, 'delete_supplier.html', {'supplier':supplier})