from django.urls import path 
from . import views 

app_name = "units"


urlpatterns = [
    path('create/', views.create_unit, name="create_unit"),
    path('list/', views.unit_list, name="unit_list"),
    path('update/<int:pk>/', views.update_unit, name="update_unit"),
    path('delete/<int:pk>/', views.delete_unit, name="delete_unit"),
    path('error/', views.error_page, name="error_page"),
]
