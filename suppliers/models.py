from django.db import models


class Supplier(models.Model):
    name=models.CharField(max_length=20, blank=False, unique=True)
    phone=models.CharField(max_length=15)
    address =models.CharField(max_length=100, blank=True, null=True)
    
    
    
    def __str__(self):
        return self.name