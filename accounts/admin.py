from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Register the Role model
admin.site.register(Role, RoleAdmin)

class CustomUserAdmin(UserAdmin):
    model = User
    # Fields to display in the user list view in admin panel
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    
    # Define the form fields in the user edit page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Role', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'role', 'is_active', 'is_staff')
        }),
    )
    filter_horizontal = ()
    list_per_page = 10

# Register the User model with the custom admin
admin.site.register(User, CustomUserAdmin)
