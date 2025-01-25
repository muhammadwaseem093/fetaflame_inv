from django import forms
from .models import OGP, OGPItem
from suppliers.models import Supplier
from units.models import Unit
from items.models import Item
from categories.models import Category

class IGPForm(forms.ModelForm):
    class Meta:
        model = OGP
        fields = [
            'ogp_number',
            'messer',
            'date',
            'vehicle_number',
            'vehicle_type',
            'driver_name',
            'driver_contact',
            'category',
            'address'
        ]
        
class OGPItemForm(forms.ModelForm):
    class Meta:
        model = OGPItem
        fields = [
            'item',
            'description',
            'unit',
            'quantity'
        ]
        
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), empty_label="Select a Unit")