from django.urls import path 
from . import views 

app_name = "employees"

urlpatterns = [
    path('create/', views.create_employee, name="create_employee"),
    path('list/', views.employee_list, name="employee_list"),
    path('update/<int:pk>/', views.update_employee, name="update_employee"),
    path('delete/<int:pk>/', views.delete_employee, name="delete_employee"),
    path('error/', views.error_page, name='error_page'),
]
