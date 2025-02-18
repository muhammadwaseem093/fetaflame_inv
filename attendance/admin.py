from django.contrib import admin
from .models import Attendance

class AttendanceAdmin(admin.ModelAdmin):
    # Define which fields to display in the list view
    list_display = ('employee', 'attendance_date', 'total_hours_display', 'is_late_display', 'is_early_leave_display', 'status')
    
    # Filters for the admin interface
    list_filter = ('attendance_date', 'status')

    # Make fields searchable
    search_fields = ('employee__name', 'attendance_date')

    # Custom methods for display in the admin panel
    def total_hours_display(self, obj):
        return f"{obj.total_hours():.2f} hrs"
    total_hours_display.short_description = "Total Hours Worked"

    def is_late_display(self, obj):
        return "Yes" if obj.is_late() else "No"
    is_late_display.short_description = "Late?"

    def is_early_leave_display(self, obj):
        return "Yes" if obj.is_early_leave() else "No"
    is_early_leave_display.short_description = "Early Leave?"

    # Customizing the list display
    total_hours_display.admin_order_field = 'check_in'  # Optional: Make it sortable by check-in time (if needed)
    is_late_display.admin_order_field = 'check_in'
    is_early_leave_display.admin_order_field = 'check_out'

admin.site.register(Attendance, AttendanceAdmin)
