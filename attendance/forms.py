from django import forms
from .models import Attendance
from employees.models import Employee

class AttendanceForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())
    class Meta:
        model = Attendance
        fields = ['employee', 'attendance_date', 'check_in', 'check_out', 'status', 'remarks', 'break_start', 'break_end']
