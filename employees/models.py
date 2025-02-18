from django.db import models
from departments.models import Department
from datetime import date

class Employee(models.Model):
    photo = models.ImageField(upload_to='employee_photos/', blank=True, null=True)
    face_encoding = models.BinaryField(blank=True, null=True)
    name = models.CharField(max_length=255,null=True, blank=True)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    cnic = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    religious = models.CharField(max_length=50, blank=True)
    marital_status = models.CharField(max_length=20, blank=True)
    current_job = models.CharField(max_length=255, blank=True, null=True)
    previous_job_title = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    current_address = models.TextField(null=True , blank=True)
    permanent_address = models.TextField(null=True , blank=True)
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    previous_job_start = models.DateField(blank=True, null=True)
    previous_job_end = models.DateField(blank=True, null=True)
    
    
    
    def save_face_encoding(self):
        """Extract and save face encoding from the uploaded image. """
        
        if self.photo:
            image_path = self.photo.path
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encoding(image)
            
            if encoding:
                self.face_encoding = np.array(encodings[0]).tobytes()
            else:
                self.face_encoding = None
                
            super().save()
            

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

    def __str__(self):
        return self.name
