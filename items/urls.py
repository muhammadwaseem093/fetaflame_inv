from django.urls import path 
from . import views 

app_name = "items"

urlpatterns = [
    path('create/', views.create_item, name="create_item"),
    path('list/', views.item_list, name="item_list"),
    path('update/<int:pk>/', views.update_item, name="update_item"),
    path('delete/<int:pk>/', views.delete_item, name="delete_item"),
    path('error/', views.error_page, name="error_page"),
]
