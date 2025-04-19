
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import global_error_page
from items.views import custom_404

handler404 = custom_404



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
    path('ogp/', include('ogp.urls')),
    path('items/', include('items.urls')),
    path('attendance/', include('attendance.urls')),
    path('error/', global_error_page, name="global_error_page"),
    path('reports/', include('reports.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
