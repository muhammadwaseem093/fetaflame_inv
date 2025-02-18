from django.urls import path 
from . import views
app_name = 'suppliers'

urlpatterns = [
    path('create/', views.create_supplier, name="create_supplier"),
    path('view/', views.supplier_list, name='supplier_list'),
    path('update/<int:pk>/', views.update_supplier, name="update_supplier"),
    path('delete/<int:pk>/' , views.delete_supplier, name="delete_supplier"),
    path('error/', views.error_page, name="error_page"),
]
