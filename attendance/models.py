from datetime import datetime, timedelta,time
from django.utils.timezone import make_aware
from django.db  import models
from employees.models import Employee

class Attendance(models.Model):
    ATTENDANCE_TYPE_CHOICES = [
        ('Check In', 'Check In'),
        ('Check Out', 'Check Out'),
        ('Break Out', 'Break Out'),
        ('Break In', 'Break In'),
        ('For Market', 'For Market'),
        ('From Market', 'From Market'),
        ('For Vendor', 'For Vendor'),
        ('From Vendor', 'From Vendor'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    attendance_type = models.CharField(max_length=50 ,choices=ATTENDANCE_TYPE_CHOICES, default="Check In")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    late_minutes = models.IntegerField(default=0, blank=True, null=True)
    status = models.CharField(max_length=50, default="Absent",choices=(('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave')))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    


    def __str__(self):
        return f"{self.employee} - {self.attendance_type} - {self.timestamp}"
    
   
