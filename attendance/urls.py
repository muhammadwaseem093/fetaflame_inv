from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('list/', views.get_daily_summary, name='attendance_list'),
    # path('list/monthly_summary', views.get_monthly_summary, name="get_monthly_sumamry"),
    path('employee_detailed/<int:employee_id>/', views.employee_detailed_attendance, name='employee_detailed_attendance'),
    path('emp_data', views.get_employee_data, name='get_employee_data'),
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('save_attendance/', views.save_attendance, name='save_attendance'),
    path('delete/<int:attendance_id>/', views.delete_attendance, name='delete_attendance'),
  
]