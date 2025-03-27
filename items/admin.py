from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_no', 'description')  # Columns to display in the list view
    search_fields = ('name', 'item_no')  # Enables search by name and item number
    list_filter = ('name',)  # Adds a filter sidebar
    ordering = ('item_no',)  # Orders items by item number
    list_editable = ('description',)  # Enables inline editing of description
    list_display_links = ('name', 'item_no')  # Clickable fields to open the detail page
    readonly_fields = ('item_no',)  # Prevents editing of item number
    fieldsets = (
        ("Item Information", {
            "fields": ("name", "item_no"),
        }),
        ("Additional Details", {
            "fields": ("description",),
            "classes": ("collapse",),  # Collapsible section in the admin panel
        }),
    )
    list_per_page = 25  # Pagination in admin panel

