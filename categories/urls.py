from django.urls import path
from . import views

app_name = "categories"  # Namespace for URL resolution

urlpatterns = [
    path('create/', views.create_category, name="create_category"),
    path('list/', views.category_list, name="category_list"),
    path('update/<int:pk>/', views.update_category, name="update_category"),
    path('delete/<int:pk>/', views.delete_category, name="delete_category"),
    path('error/', views.error_page, name="error_page"),  
]
