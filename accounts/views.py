from django.shortcuts import render, redirect
from .models import User, Role
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import UserCreationForm
from utils.decorators import role_required
from igp.models import IGP
from ogp.models import OGP
from employees.models import Employee
import datetime
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from datetime import date


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
        else:
            form = UserCreationForm()
        return render(request, 'register.html', {'form':form})
    
    
def login_view(request):
    if request.method == 'POST':
        username=request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            if user.role.name == Role.ADMIN:
                return redirect('admin_dashboard')
            elif user.role.name == Role.HR:
                return redirect('hr_dashboard')
            elif user.role.name == Role.STAFF:
                return redirect('staff_dashboard')
            else:
                return redirect('register_view')
            
        else:
            return render(request, 'login.html', {'error':'Invalid credential'})
    return render(request, 'login.html')


@login_required
@role_required('admin')
def admin_dashboard(request):
    today = date.today()

    context = {
        'total_employees': 150,
        'present_today': 120,
        'absent_today': 20,
        'late_today': 10,
        'todays_ogp': 5,
        'pending_igp': 3,
        'pending_ogp': 2,
        'recent_logs': [
            {'activity_type': 'New IGP', 'description': 'Received 100 items', 'timestamp': '10:30 AM'},
            {'activity_type': 'New OGP', 'description': 'Shipped 80 items', 'timestamp': '11:00 AM'},
            {'activity_type': 'New Supplier', 'description': 'ABC Ltd. added', 'timestamp': '12:15 PM'},
            {'activity_type': 'New Vendor', 'description': 'XYZ Pvt. Ltd. added', 'timestamp': '1:00 PM'},
        ]
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
@role_required('hr')
def hr_dashboard(request):
    today = datetime.date.today()
    # igp_count_today = IGP.objects.filter(created_at__date=today).count()
    emp_count_total = Employee.objects.all().count()
    # ogp_count_today = OGP.objects.filter(created_at__date=today).count()
    # ogp_count_total = OGP.objects.all().count()
    return render(request, 'dashboard/hr_dashboard.html', {'emp_count_total':emp_count_total})

@login_required
@role_required('staff')
def staff_dashboard(request):
    
    today = datetime.date.today()
    igp_count_today = IGP.objects.filter(created_at__date=today).count()
    igp_count_total = IGP.objects.all().count()
    ogp_count_today = OGP.objects.filter(created_at__date=today).count()
    ogp_count_total = OGP.objects.all().count()
    return render(request, 'dashboard/staff_dashboard.html', { 'igp_count_total':igp_count_total, 'ogp_count_total':ogp_count_total, 'igp_count_today':igp_count_today, 'ogp_count_today':ogp_count_today})


def home(request):
    if request.user.is_authenticated:
        if request.user.role.name == Role.ADMIN:
            return redirect('admin_dashboard')
        elif request.user.role.name == Role.HR:
            return redirect('hr_dashboard')
        elif request.user.role.name == Role.STAFF:
            return redirect('staff_dashboard')
        else:
            return redirect('register_view')
    return render(request, 'base.html')

@require_POST
def logout_view(request):
    logout(request)
    return redirect('login_view')

def global_error_page(request):
    return render(request, 'global/error.html')