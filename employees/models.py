from django.db import models
from departments.models import Department
from datetime import date



class Employee(models.Model):
    photo = models.ImageField(upload_to='', blank=True, null=True)
    stauts = models.CharField(max_length=20, choices=[('active', 'Active'), ('on_leave', 'On Leave'),('retired','Retired'),('terminated','Terminated')], default='Active')
    name = models.CharField(max_length=255,null=True, blank=True)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    cnic = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'),('Others','Others')], default='Male')
    religious = models.CharField(max_length=20, choices=[('Islam', 'Islam'), ('Christianity', 'Christianity'), ('Hinduism', 'Hinduism'), ('Others', 'Others')], default='Islam')
    marital_status = models.CharField(max_length=20, choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')], default='Single')
    current_job = models.CharField(max_length=255, blank=True, null=True)
    previous_job_title = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    current_address = models.TextField(null=True , blank=True)
    permanent_address = models.TextField(null=True , blank=True)
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    previous_job_start = models.DateField(blank=True, null=True)
    previous_job_end = models.DateField(blank=True, null=True)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    traveling_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    food_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    marriage_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    house_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    casual_leave = models.IntegerField(blank=True, null=True)
    sick_leave = models.IntegerField(blank=True, null=True)
    annual_leave = models.IntegerField(blank=True, null=True)
    medical_leave = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True ,null=True , blank=True) 
    updated_at = models.DateTimeField(auto_now=True, null=True , blank=True)
    

    def calculate_previous_job_duration(self):
        """
        Calculates the duration of the previous job at runtime.
        """
        if self.previous_job_start and self.previous_job_end:
            delta = self.previous_job_end - self.previous_job_start
            years = delta.days // 365
            months = (delta.days % 365) // 30
            days = (delta.days % 365) % 30
            return f"{years}y {months}m {days}d"
        return "N/A"

    def clean_cnic(self):
        cnic = self.cnic 
        if cnic and not self.is_valid_cnic(cnic):
            raise ValidationError("Invalid CNIC Format.")
        return cnic 
    
    def clean_contact_no(self):
        contact_no = self.contact_no 
        if contact_no  and not self.is_valid_contact_no(contact_no):
            raise ValidationError("Invalid Contact Number Format")
        return contact_no 
    
    def is_valid_cnic(self, cnic):
        cnic = "".join(filter(str.isdigit, cnic))
        return len(cnic) == 13
    
    def is_valid_contact_no(self, contact_no):
        contact_no = "".join(filter(str.isdigit, contact_no))
        return len(contact_no) == 11
    
    def __str__(self):
        return self.name
