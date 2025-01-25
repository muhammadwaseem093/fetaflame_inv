from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from utils.decorators import role_required
from vendor.models import Vendor
from .models import OGP,OGPItem
from .forms import OGPForm, OGPItemForm
from units.models import Unit
from categories.models import Category
from items.models import Item
from utils.helpers import search_and_paginate


@login_required
@role_required('staff','hr','admin')
def ogp_list(request):
    filters = {
        'ogp_number':'ogp_number',
        'messer__name':'messer',
    }
    
    ogp_list, search_params = search_and_paginate(
        request,
        model = OGP,
        filters=filters,
        ordering='-date',
        per_page=10,
    )
    
    return render(request, 'ogp_list.html',{
        'ogp_list':ogp_list,
        'search_params':search_params,
        'search_active':bool(search_params),
    })



@login_required
@role_required('staff','hr','admin')
def ogp_item_list(request, ogp_number):
    try:
        selected_ogp = OGP.objects.get(ogp_number=ogp_number)
    except OGP.DoesNotExist:
        raise Http404('OGP Not Found!')
    ogp_items = OGPItem.objects.filter(ogp__ogp_number=selected_ogp.ogp_number)
    
    context = {
        'ogp_number':selected_ogp.ogp_number,
        'messer_name':selected_ogp.messer.name,
        'category':selected_ogp.category,
        'ogp_items':ogp_items,
    }
    
    return render(request, 'ogp_items_list.html',context)


@login_required
@role_required('staff','hr','admin')
def create_ogp(request):
    vendors = Vendor.objects.all()
    categories = Category.objects.all()
    if request.method  == "POST":
        form = OGPForm(request.POST)
        if form.is_valid():
            ogp = form.save()
            ogp_number = ogp.ogp_number
            return redirect(reverse('create_ogp_items')+f"?ogp_number={ogp_number}")
    else:
        form = OGPForm()
    return render(request, 'create_ogp.html', {'form':form, 'vendors':vendors, 'categories':categories})


@login_required
@role_required('staff','hr','admin')
def create_ogp_items(request):
    ogp_number = request.GET.get('ogp_number') or request.POST.get('ogp_number')
    if not ogp_number:
        raise Http404('OGP Number is required')
    ogp = get_object_or_404(OGP, ogp_number=ogp_number)
    items = Item.objects.all()
    units = Unit.objects.all()
    
    if request.method == "POST":
        item_forms  = []
        num_items = len(request.POST) // 4
        
        for i in range(1, num_items + 1):
            item_key = f'item_{i}'
            description_key = f'description_{i}'
            unit_key = f'unit_{i}'
            quantity_key = f'quantity_{i}'
            
            
            item_id = request.POST.get(item_key)
            description = request.POST.get(description_key)
            unit_id = request.POST.get(unit_key)
            quantity = request.POST.get(quantity_key)
            
            if item_id: 
                data = {
                    'item':item_id,
                    'description':description,
                    'unit':unit_id,
                    'quantity':quantity,
                }
                
                form = OGPItemForm(data)
                if form.is_valid():
                    ogp_item = form.save(commit=False)
                    ogp_item.ogp = ogp 
                    ogp_item.save()
                else:
                    for field, error in form.errors.items():
                        messages.error(request, f"{field}: {error}")
                    item_forms.append(form)
                    return JsonResponse({'success':False, 'message':'Validation Error'})
        return redirect('ogp_list')
    else:
        form = OGPItemForm()
    return render(request, 'create_ogp_items.html', {'form':form, 'items':items, 'units':units,"ogp_number":ogp_number, "range":range(1,11)})



@login_required
@role_required('staff','hr','admin')
def update_ogp(request, pk):
    ogp = get_object_or_404(OGP, pk=pk)
    vendors = Vendor.objects.all()
    categories = Category.objects.all()
    if request.method == "POST":
        form = OGPForm(request.POST, instance=ogp)
        if form.is_valid():
            ogp = form.save()
            ogp_number = ogp.ogp_number
            return redirect(reverse('update_ogp_items', kwargs={'ogp_number':ogp_number}))
    else:
        form = OGPForm(instance=ogp)
    return render(request, 'update_ogp.html', {'form':form, 'vendors':vendors, 'categories':categories, 'ogp':ogp})


@login_required
@role_required('staff','hr','admin')
def update_ogp_items(request, ogp_number):
    ogp = get_object_or_404(OGP, ogp_number=ogp_number)
    items = Item.objects.all()
    units = Unit.objects.all()
    
    if request.method == "POST":
        num_items = len(request.POST) // 4
        for i in range(1, num_items + 1):
            item_key = f'item_{i}'
            description_key = f'description_{i}'
            unit_key = f'unit_{i}'
            quantity_key = f'quantity_{i}'
            
            item_id = request.POST.get(item_key)
            description = request.POST.get(description_key)
            unit = request.POST.get(unit_key)
            quantity = request.POST.get(quantity_key)
            
            if item_id:
                ogp_items = OGPItem.objects.filter(ogp=ogp, item_id=item_id)
                if ogp_items.exists():
                    for ogp_item in ogp_items:
                        ogp_item.description = description
                        ogp_item.unit_id = unit
                        ogp_item.quantity = quantity
                        ogp_item.save()
                
        return redirect('ogp_list')
    else:
        ogp_items = OGPItem.objects.filter(ogp=ogp)
    return render(request, 'update_ogp_items.html',
                { 'ogp_number':ogp_number,
                'items':items,
                'units':units,
                'ogp_items':ogp_items,
                })
            
            
            
@login_required
@role_required('staff','hr','admin')
def delete_ogp(request, pk):
    try:
        ogp = OGP.objects.get(pk=pk)
    except OGP.DoesNotExist:
        raise Http404('OGP Not Found!')
    if request.method == 'POST':
        ogp.delete()
        messages.success(request, 'OGP Deleted Successfully')
        return redirect('ogp_list')
    return render(request, 'delete_ogp.html', {'ogp':ogp})