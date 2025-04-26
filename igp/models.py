from django.conf import settings
from django.db import models
from suppliers.models import Supplier 
from items.models import Item 
from units.models import Unit
from django.utils import timezone
from categories.models import Category
from accounts.models import User
from django.utils.timezone import now
from django.db.models import Max



class IGP(models.Model): 
    igp_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    messer = models.ForeignKey(Supplier,on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)
    vehicle_type = models.CharField(max_length=50, blank=True, null=True)
    driver_name = models.CharField(max_length=50, blank=True, null=True)
    driver_contact = models.CharField(max_length=15, blank=True, null=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    address=models.CharField(max_length=100, null=False, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True )
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.igp_number: 
            last_igp = IGP.objects.aggregate(max_num=Max('id'))['max_num'] or 0
            next_id = last_igp + 1
            self.igp_number = f"IGP-{next_id:05d}"
        self.updated_at = now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"IGP {self.igp_number} - {self.messer}"
    
    
    
class IGPItem(models.Model):
    igp = models.ForeignKey(IGP, on_delete=models.CASCADE, related_name="items")
    item=models.ForeignKey(Item, on_delete=models.CASCADE)
    description=models.TextField(blank=True, null=True)
    unit=models.ForeignKey(Unit, on_delete=models.CASCADE)
    quantity=models.DecimalField(max_digits=10, decimal_places=2)
    
    def clean_item(self):
        item_id = self.cleaned_data.get('item')
        if not Item.objects.filter(id=item_id).exists():
            raise forms.validationError("Item Does Not Exists")
        return item_id
    
    def clean_unit(self):
        unit_name=self.cleaned_data.get('unit')
        try:
            unit = Unit.objects.get(name=unit_name)
        except Unit.DoesNotExist:
            raise ValidationError(f"The Unit '{unit_name}' does not exist")
        return unit
    
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than 0")
        return quantity
    
  
    
    
    
    def __str__(self):
        return f"{self.igp} - {self.item} {self.quantity} {self.unit}"