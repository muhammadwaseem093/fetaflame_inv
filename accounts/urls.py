
from django.contrib import admin
from django.urls import path
from .views import register_view, login_view,admin_dashboard, hr_dashboard, staff_dashboard

urlpatterns = [
    path("register/", register_view, name="register_view"),
    path('login/', login_view, name="login_view"),
    path('admin/', admin_dashboard, name="admin_dashboard"),
    path('hr/', hr_dashboard, name="hr_dashboard"),
    path('staff_dashboard/', staff_dashboard, name="staff_dashboard")
    
]
