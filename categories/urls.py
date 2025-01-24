from django.urls import path 
from . import views 


urlpatterns = [
    path('create/', views.create_category, name="create_category"),
    path('list/', views.category_list, name="category_list"),
    path('update/<int:pk>/', views.update_category, name="update_category"),
    path('delete/<int:pk>/', views.delete_category, name="delete_category"),
]
