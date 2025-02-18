from django.urls import path 
from . import views

app_name = "departments"

urlpatterns = [
    path('create/', views.create_dept, name="create_dept"),
    path('view/', views.view_dept, name="view_dept"),
    path('update/<int:pk>/', views.update_dept, name="update_dept"),
    path('delete/<int:pk>/', views.delete_dept, name="delete_dept"),
    path('error/', views.error_page, name="error_page"),
]