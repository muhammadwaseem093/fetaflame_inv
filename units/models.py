from django.db import models

class Unit(models.Model):
    name=models.CharField(max_length=50, null=False, blank=False, unique=True)
    description=models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name