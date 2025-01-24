from django.urls import path 
from . import views 

urlpatterns = [
    path('create/', views.create_igp, name="create_igp"),
    path('list/',views.igp_list, name="igp_list"),
    path('create-item/', views.create_igp_items, name="create_igp_items"),
    path('igp-items/<str:igp_number>/', views.igp_item_list, name='igp_item_list'),
    # path('udpate/<int:pk>/', views.update_igp, name="update_igp"),
#     path('delete/<int:pk>/',views.delete_igp, name="delete_igp"),
# ]
]
