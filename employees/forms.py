# employees/forms.py
from django import forms
from .models import Employee
from departments.models import Department
from django.core.validators import RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
import datetime

class EmployeeForm(forms.ModelForm):
    # Custom field validations
    cnic = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{7}-\d{1}$',
                message='CNIC must be in the format: 00000-0000000-0'
            )
        ],
        required=True
    )
    
    contact_no = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        required=True
    )

    photo = forms.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            lambda value: ValidationError('Max file size 2MB') if value and value.size > 2*1024*1024 else None
        ]
    )
    
    captured_image = forms.CharField(widget=forms.HiddenInput(), required=False)

    religious = forms.ChoiceField(
        choices=[
            ('Islam', 'Islam'),
            ('Christianity', 'Christianity'),
            ('Hinduism', 'Hinduism'),
            ('Sikhism', 'Sikhism'),
            ('Judaism', 'Judaism'),
            ('Buddhism', 'Buddhism'),
            ('Other', 'Other'),
        ],
        required=True
    )

    marital_status = forms.ChoiceField(
        choices=[
            ('Single', 'Single'),
            ('Married', 'Married'),
            ('Divorced', 'Divorced'),
        ],
        required=True
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        empty_label="Select Department"
    )

    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'max': datetime.date.today()}),
            'previous_job_start': forms.DateInput(attrs={'type': 'date'}),
            'previous_job_end': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # Date validation
        previous_job_start = cleaned_data.get('previous_job_start')
        previous_job_end = cleaned_data.get('previous_job_end')
        
        if previous_job_start and previous_job_end:
            if previous_job_end < previous_job_start:
                raise ValidationError({
                    'previous_job_end': 'End date cannot be earlier than start date'
                })

        # Conditional required fields for previous job
        previous_job_fields = [
            'previous_job_title',
            'previous_job_start',
            'previous_job_end'
        ]
        
        if any(cleaned_data.get(field) for field in previous_job_fields):
            for field in previous_job_fields:
                if not cleaned_data.get(field):
                    raise ValidationError({
                        field: 'All previous job fields are required when providing any previous job information'
                    })

        return cleaned_data

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob and dob > datetime.date.today():
            raise ValidationError("Date of birth cannot be in the future")
        return dob