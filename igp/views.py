from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.db.models import Count
from django.contrib import messages 
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from utils.decorators import role_required
from suppliers.models import Supplier
from .models import IGP,IGPItem
from .forms import IGPForm, IGPItemForm
from units.models import Unit
from categories.models import Category
from items.models import Item 
from utils.helpers import search_and_paginate


@login_required
@role_required('staff','hr','admin')
def igp_list(request):
    
    filters = {
        'igp_number': 'igp_number',
        'messer__name':'messer',
    }
    
    
    igp_list, search_params = search_and_paginate(
        request,
        model=IGP,
        filters=filters,
        ordering='-date',
        per_page=10,
    )
    
    
    return render(request, 'igp_list.html', {
        'igp_list': igp_list,
        'search_params': search_params,  
        'search_active': bool(search_params), 
    })

@login_required
@role_required('staff', 'hr', 'admin')
def igp_item_list(request, igp_number):
    try:
        selected_igp = IGP.objects.get(igp_number=igp_number)
    except IGP.DoesNotExist:
        raise Http404("IGP not found")

    igp_items = IGPItem.objects.filter(igp__igp_number=selected_igp.igp_number)

    # Prepare the context data for rendering
    context = {
        'igp_number': selected_igp.igp_number,
        'messer_name': selected_igp.messer.name,
        'category': selected_igp.category,
        'igp_items': igp_items,  # List of items for the selected IGP
    }

    # Render the template with the context data
    return render(request, 'items_list.html', context)

@login_required
@role_required('staff','hr','admin')
def igp_items_list(request):
    igpitem = IGPItem.objects.all()
    return render(request, 'items_list.html', {"igpitem":igpitem})


@login_required
@role_required('staff','hr','admin')
def create_igp(request):
    suppliers = Supplier.objects.all()
    categories = Category.objects.all()
    if request.method == "POST":
        form = IGPForm(request.POST)
        if form.is_valid():
            igp = form.save()
            igp_number = igp.igp_number
            return redirect(reverse("create_igp_items")+f"?igp_number={igp_number}")
        else:
            messages.error(request, "Validation Error ")
    else:
        form = IGPForm()
    return render(request, "create_igp.html", {"form":form, "suppliers":suppliers, "categories":categories})

@login_required
@role_required('staff', 'hr', 'admin')
def create_igp_items(request):
    igp_number = request.GET.get('igp_number') or request.POST.get('igp_number')
    if not igp_number:
        return JsonResponse({'success': False, 'message': 'No IGP Number Provided'})

    igp = get_object_or_404(IGP, igp_number=igp_number)
    items = Item.objects.all()
    units = Unit.objects.all()

    if request.method == 'POST':
        item_forms = []
        num_items = len(request.POST) // 4  # Calculate how many rows were added based on the fields sent

        for i in range(1, num_items + 1):
            item_key = f'item_{i}'
            description_key = f'description_{i}'
            unit_key = f'unit_{i}'
            quantity_key = f'quantity_{i}'

            # Get values from the POST request for each row
            item_id = request.POST.get(item_key)
            description = request.POST.get(description_key, '')
            unit = request.POST.get(unit_key)
            quantity = request.POST.get(quantity_key)

            if item_id:
                data = {
                    'item': item_id,
                    'description': description,
                    'unit': unit,
                    'quantity': quantity
                }

                form = IGPItemForm(data)
                if form.is_valid():
                    igp_item = form.save(commit=False)
                    igp_item.igp = igp
                    igp_item.save()
                else:
                    # If the form is invalid, log the errors
                    for field, error in form.errors.items():
                        print(f"Field: {field} - Errors: {error}")
                    item_forms.append(form)
                    return JsonResponse({"success": False, "message": f"Invalid data for item {i}. Errors: {form.errors}"}, status=400)

        return redirect('igp_list')  # Redirect to list page after saving all items

    else:
        form = IGPItemForm()

    return render(request, 'create_igp_item.html', {
        'form': form,
        'range': range(1, 11),  # Allow a maximum of 10 rows
        'items': items,
        'units': units,
        'igp_number': igp_number
    })


@login_required
@role_required('staff','hr','admin')
def update_igp(request, pk):
    igp = IGP.objects.get(id=pk)
    suppliers = Supplier.objects.all()
    categories = Category.objects.all()
    if request.method == "POST":
        form = IGPForm(request.POST, instance=igp)
        if form.is_valid():
            igp = form.save()
            igp_number = igp.igp_number
            return redirect(reverse("update_igp_items", kwargs={'igp_number': igp_number}))
        else:
            messages.error(request, "Validation Error ")
    else:
        form = IGPForm(instance=igp)
    return render(request, "edit_igp.html", {"form":form, "suppliers":suppliers, "categories":categories,"igp":igp})



@login_required
@role_required('staff', 'hr', 'admin')
def update_igp_items(request, igp_number):
    igp = get_object_or_404(IGP, igp_number=igp_number)
    items = Item.objects.all()
    units = Unit.objects.all()

    if request.method == 'POST':
        num_items = len(request.POST) // 4  # Calculate number of items submitted based on the number of fields

        for i in range(1, num_items + 1):
            item_key = f'item_{i}'
            description_key = f'description_{i}'
            unit_key = f'unit_{i}'
            quantity_key = f'quantity_{i}'

            item_id = request.POST.get(item_key)
            description = request.POST.get(description_key, '')
            unit = request.POST.get(unit_key)
            quantity = request.POST.get(quantity_key)

            if item_id:
                igp_items = IGPItem.objects.filter(igp=igp, item_id=item_id)
                if igp_items.exists():
                    for igp_item in igp_items:
                        igp_item.description = description
                        igp_item.unit_id = unit
                        igp_item.quantity = quantity
                        igp_item.save()

        return redirect('igp_list')  # Redirect to the list page after successful update

    else:
        # Fetch IGP items to pre-populate the form
        igp_items = IGPItem.objects.filter(igp=igp)
        return render(request, 'update_igp_items.html', {
            'igp_number': igp_number,
            'items': items,
            'units': units,
            'igp_items': igp_items
        })

@login_required
@role_required('hr','admin')
def delete_igp(request,pk):
    try:
        igp = IGP.objects.get(id=pk)
    except IGP.DoesNotExist:
        raise Http404('NO IGP Found!!!')
    if request.method == "POST":
        igp.delete()
        messages.success(request,'Igp with items deleted')
        return redirect('igp_list')
    return render(request, 'delete_igp.html', {'igp':igp})