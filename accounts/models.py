from django.db import models
from django.contrib.auth.models import AbstractUser 

class Role(models.Model):
    ADMIN = 'admin'
    HR = 'hr'
    STAFF = 'staff'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (HR, 'HR'),
        (STAFF, 'Staff'),
    ]
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, default=STAFF)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.role.name if self.role else 'No Role'}"