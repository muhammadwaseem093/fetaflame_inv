from django import forms 
from .models import IGP, IGPItem
from suppliers.models import Supplier
from units.models import Unit
from items.models import Item 
from categories.models import Category

class IGPForm(forms.ModelForm):
    class Meta:
        model = IGP 
        fields = [
            'messer',
            'date',
            'vehicle_number',
            'vehicle_type',
            'driver_name',
            'driver_contact',
            'category',
            'address',
            ]
        exclude = ['igp_number', 'created_at', 'created_by', 'updated_at']
class IGPItemForm(forms.ModelForm):
    class Meta:
        model = IGPItem 
        fields= [
            'item',
            'description',
            'unit',
            'quantity'
        ]
        
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), empty_label="Select a Unit")