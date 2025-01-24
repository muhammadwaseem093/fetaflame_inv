from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required
from utils.decorators import role_required
from .models import Category
from .forms import CategoryForm


@login_required
@role_required('staff','hr','admin')
def category_list(request):
    category = Category.objects.all()
    return render(request, 'category_list.html', {"category":category})

@login_required
@role_required('staff','hr','admin')
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Created Successfully!")
            return redirect("category_list")
        else:
            messages.error(request, "Category Creation Failed")
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {"form":form})



@login_required
@role_required('staff',"hr","admin")
def update_category(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated Successfully!")
            return redirect("category_list")
        else:
            messages.error(request, "Category update Failed")
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {"form":form, "category":category})


@login_required
@role_required('admin',"hr")
def delete_category(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        raise Http404('Category Does NOt Exist')
    if request.method =="POST":
        category.delete()
        messages.success(request, "Category Deleted Successfully!")
        return redirect("category_list")
    return render(request, "delete_category.html", {"category":category})
