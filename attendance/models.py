from datetime import datetime, timedelta,time
from django.utils.timezone import make_aware
from django.db  import models
from employees.models import Employee
from django.utils import timezone
from datetime import datetime, time 


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
    timestamp = models.DateTimeField( blank=True, null=True)
    late_minutes = models.IntegerField(default=0, blank=True, null=True)
    status = models.CharField(max_length=50, default="Absent",choices=(('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave')))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    


    def is_late(self):
        if not self.timestamp:
            return 0

        # Convert timestamp to local timezone
        local_checkin = timezone.localtime(self.timestamp)

        # Create scheduled time in local timezone
        scheduled_time_local = datetime.combine(local_checkin.date(), time(8, 0, 0))
        
        # Convert the scheduled time to aware datetime
        scheduled_time_aware = make_aware(scheduled_time_local, timezone.get_current_timezone())

        # Compare with the check-in time
        if self.timestamp > scheduled_time_aware:
            diff = self.timestamp - scheduled_time_aware
            late_minutes = int(diff.total_seconds() / 60)
            print(f"[DEBUG] Late by: {late_minutes} min")
            return late_minutes
        
        return 0

    
    def save(self, *args, **kwargs):
        if self.attendance_type == 'Check In':
            self.late_minutes = self.is_late()
            print(f"[DEBUG - SAVE] Calculated Late Minutes for {self.employee.name}: {self.late_minutes}")
        else:
            self.late_minutes = 0
        super().save(*args, **kwargs)
 


    def __str__(self):
        return f"{self.employee} - {self.attendance_type} - {self.timestamp}"
    

