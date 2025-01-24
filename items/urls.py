from django.urls import path 
from . import views 

urlpatterns = [
    path('create/', views.create_item, name="create_item"),
    path('list/', views.item_list, name="item_list"),
    path('update/<int:pk>/', views.update_item, name="update_item"),
    path('delete/<int:pk>/', views.delete_item, name="delete_item"),
]
