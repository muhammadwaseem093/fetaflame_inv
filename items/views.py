from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages 
from django.http import Http404
from django.contrib.auth.decorators import login_required
from utils.decorators import role_required
from .models import Item 
from .forms import ItemForm
from utils.helpers import search_and_paginate


@login_required
@role_required('staff','hr','admin')
def item_list(request):
    filters = {
        "item_no":'item_no',
    }
    
    item_list , search_params = search_and_paginate(
        request,
        model=Item,
        filters=filters,
        ordering='item_no',
        per_page=10,
    )
    
    return render(request, 'item_list.html',{
        'item_list':item_list,
        'search_params':search_params,
        'search_active': bool(search_params),
    })


@login_required
@role_required('staff','hr','admin')
def create_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item Created Successfully!')
            return redirect('items:item_list')
        else:
            messages.error(request, 'Item Creation Failed')
    else:
        form = ItemForm()
    return render(request, 'create_item.html', {"form":form})


@login_required
@role_required('staff','hr','admin')
def update_item(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request,'Item Updated Successfully')
            return redirect('items:item_list')
        else:
            messages.error(request, 'Item Update Failed')
    else:
        form = ItemForm(instance=item)
    return render(request, 'edit_item.html', {"form":form , "item":item})


@login_required
@role_required('hr','admin')
def delete_item(request, pk):
    try:
        item = Item.objects.get(id=pk)
    except Item.DoesNotExist:
        raise Http404('Item Does Not Exist')
    if request.method == "POST":
        item.delete()
        messages.success(request, 'Item Deleted Successfully!')
        return redirect('items:item_list')
    return render(request, 'delete_item.html', {"item":item})

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def error_page(request):
    return render(request, 'error.html')