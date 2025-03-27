
from django.contrib import admin
from django.urls import path
from . import  views

urlpatterns = [
    path("register/", views.register_view, name="register_view"),
    path('login/', views.login_view, name="login_view"),
    path('admin/', views.admin_dashboard, name="admin_dashboard"),
    path('hr/', views.hr_dashboard, name="hr_dashboard"),
    path('staff_dashboard/', views.staff_dashboard, name="staff_dashboard"),
    path('home/', views.home, name="home"),
    path('logout/', views.logout_view, name="logout_view"),
    
]
