
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('employees/', include('employees.urls')),
    path('departments/', include('departments.urls')),
    path('suppliers/', include('suppliers.urls')),
    path('vendor/', include('vendor.urls')),
    path('units/', include('units.urls')),
    path('categories/', include('categories.urls')),
    path('igp/', include('igp.urls')),
    path('items/', include('items.urls')),
]
