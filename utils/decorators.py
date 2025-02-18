from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect 
from django.contrib import messages 
from django.urls import reverse

def role_required(*role_names):
    def check_role(user):
        return user.role is not None and user.role.name in role_names
    
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not check_role(request.user):
                messages.error(request, "You are not authorized to access this page.")
                
                # Dynamically find the app namespace
                app_name = request.resolver_match.app_name
                
                if app_name:
                    return redirect(reverse(f'{app_name}:error_page'))  # Redirects to app-specific error page
                else:
                    return redirect(reverse('global_error_page'))  # Fallback

            return view_func(request, *args, **kwargs)
        
        return _wrapped_view
    return decorator
