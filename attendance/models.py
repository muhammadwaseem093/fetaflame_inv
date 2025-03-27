from datetime import datetime, timedelta
from django.db  import models
from employees.models import Employee

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attendance_type = models.CharField(max_length=50 , default="Check In")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    


    def __str__(self):
        return f"{self.employee} - {self.attendance_type}"
