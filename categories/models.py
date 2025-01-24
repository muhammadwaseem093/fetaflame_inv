from django.db import models

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=30, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name