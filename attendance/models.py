from datetime import datetime, timedelta
from django.db  import models
from employees.models import Employee

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attendance_date = models.DateField(default=datetime.today)
    check_in = models.TimeField(default=datetime.now().time())
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, default='Present')
    remarks = models.TextField(blank=True, null=True)
    break_start = models.TimeField(null=True, blank=True)
    break_end = models.TimeField(null=True, blank=True)

    def clean(self):
        """Optional: Validate check-out time should be after check-in"""
        if self.check_out <= self.check_in:
            raise ValidationError('Check-out time must be after check-in time')

    def total_hours(self):
        """Calculate total hours worked by the employee."""
        check_in_time = datetime.combine(datetime.today(), self.check_in)
        check_out_time = datetime.combine(datetime.today(), self.check_out)
        total_time = check_out_time - check_in_time
        return total_time.total_seconds() / 3600  
    def is_late(self):
        """Determine if the employee is late based on a standard check-in time (e.g., 9 AM)."""
        standard_check_in = datetime.strptime("09:00:00", "%H:%M:%S").time()
        return self.check_in > standard_check_in

    def is_early_leave(self):
        """Determine if the employee left early based on a standard check-out time (e.g., 5 PM)."""
        standard_check_out = datetime.strptime("17:00:00", "%H:%M:%S").time()
        return self.check_out < standard_check_out

    def __str__(self):
        return f"{self.employee} - {self.attendance_date}"
