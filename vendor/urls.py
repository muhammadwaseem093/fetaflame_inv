from django.urls import path 
from .  import views

app_name = 'vendor'

urlpatterns = [
    path('create/', views.create_vendor, name="create_vendor"),
    path('list/', views.vendor_list, name="vendor_list"),
    path('update/<int:pk>/',views.update_vendor, name="update_vendor" ),
    path('delete/<int:pk>/', views.delete_vendor, name="delete_vendor"),
    path('error/', views.error_page, name="error_page"),
]
