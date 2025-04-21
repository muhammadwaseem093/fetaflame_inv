from datetime import datetime, timedelta
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
    


    def __str__(self):
        return f"{self.employee} - {self.attendance_type} - {self.timestamp}"
    
    def is_late(self):
        """ check if the employee is late (after 8:00 AM) """
        if self.attendance_type == "Check In" and self.employee.status == "active":
            duty_start_time = time(8,0,0)
            if self.timestamp.time() > duty_start_time:
                late_duration = (self.timestamp - datetime.combine(self.timestamp.date(), duty_start_time))
                return int(late_duration.total_seconds() / 60)
        return 0
        
