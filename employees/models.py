from django.db import models
from departments.models  import Department

class Employee(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name=models.CharField(max_length=50, null=False, blank=False)
    mobile=models.CharField(max_length=20)
    address=models.CharField(max_length=50, null=True, blank=True)
    cnic=models.CharField(max_length=20, null=True, blank=True)
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    designation=models.CharField(max_length=50, null=True,blank=True)
    
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.department} - {self.designation}"
