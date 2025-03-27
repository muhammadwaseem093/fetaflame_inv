from django.urls import path
from . import views 

urlpatterns = [
    path('create/', views.create_ogp, name="create_ogp"),
    path('list/',views.ogp_list, name="ogp_list"),
    path('create-item/', views.create_ogp_items, name="create_ogp_items"),
    path('ogp-items/<str:ogp_number>/', views.ogp_item_list, name='ogp_item_list'),
    path('udpate/<int:pk>/', views.update_ogp, name="update_ogp"),
    path('update-ogp-items/<int:ogp_number>/', views.update_ogp_items, name='update_ogp_items'),
    path('delete/<int:pk>/',views.delete_ogp, name="delete_ogp"),
    path('error/', views.error_page, name='error_page'),
    
    
]