from django.urls import path 
from . import views 


urlpatterns = [
    path('create/', views.create_igp, name="create_igp"),
     path('create-item/', views.create_igp_items, name="create_igp_items"),
    path('list/',views.igp_list, name="igp_list"),
    path('igp-items/<str:igp_number>/', views.igp_item_list, name='igp_item_list'),
    path('udpate/<int:pk>/', views.update_igp, name="update_igp"),
    path('update-igp-items/<int:igp_number>/', views.update_igp_items, name='update_igp_items'),
    path('delete/<int:pk>/',views.delete_igp, name="delete_igp"),
    path('error/', views.error_page, name="error_page"),
# ]
]
