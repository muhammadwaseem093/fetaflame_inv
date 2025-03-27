from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Show these fields in the admin list view
    search_fields = ('name',)  # Enable search by name
    list_filter = ('name',)  # Add filter option in admin panel
    ordering = ('name',)  # Default sorting by name
    list_per_page = 20  # Pagination in admin panel

