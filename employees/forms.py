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
            'basic_salary',
            'traveling_allowance',
            'medical_allowance',
            'food_allowance',
            'marriage_allowance',
            'house_allowance',
            'casual_leave',
            'sick_leave',
            'annual_leave',
            'medical_leave',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Enter Name'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Father Name'}),
            'cnic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter CNIC'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Enter Date of Birth'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'religious': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Religious'}),
            'marital_status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Marital Status'}),
            'current_job': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Current Job'}),
            'previous_job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Previous Job Title'}),
            'department': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Department'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Designation'}),
            'current_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Current Address'}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Permanent Address'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Number'}),
            'previous_job_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Enter Previous Job Start Date'}),
            'previous_job_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Enter Previous Job End Date'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Basic Salary'}),
            'traveling_allowance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Traveling Allowance'}),
            'medical_allowance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Medical Allowance'}),
            'food_allowance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Food Allowance'}),
            'marriage_allowance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Marriage Allowance'}),
            'house_allowance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter House Allowance'}),
            'casual_leave': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Casual Leave'}),
            'sick_leave': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Sick Leave'}),
            'annual_leave': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Annual Leave'}),
            'medical_leave': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Medical Leave'}),
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
