from django.db import models


class Item(models.Model):
    name=models.CharField(max_length=50, blank=True, null=True)
    item_no = models.CharField(max_length=50, unique=True, db_index=True, default=0)
    description=models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.item_no}"