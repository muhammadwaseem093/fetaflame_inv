from django import forms
from .models import Employee
from django.core.exceptions import ValidationError

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'photo',
            'name',
            'father_name',
            'cnic',
            'dob',
            'gender',
            'religious', 
            'marital_status',
            'current_job',
            'previous_job_title',
            'department',
            'designation',
            'current_address',
            'permanent_address',
            'contact_no',
            'previous_job_start',
            'previous_job_end',
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        
        def clean_cnic(self):
            cnic = self.cleaned_data.get('cnic')
            if cnic and not self.instance.is_valid_cnic(cnic):
                raise ValidationError("Invalid CNIC Format")
            return cnic
        
        def clean_contact_no(self):
            contact_no = self.cleaned_data.get('contact_no')
            if contact_no and not self.instance.is_valid_contact_no(contact_no):
                raise ValidationError("Invalid Contact Number format.")
            return contact_no
