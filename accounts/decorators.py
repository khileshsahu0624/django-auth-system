from django.contrib.auth.decorators import user_passes_test
from .models import User

def admin_required(function=None, redirect_field_name='next', login_url='login'):
    """
    Decorator for views that checks that the user is logged in and has either
    the SUPER_ADMIN or ADMIN role.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.role in [User.Role.SUPER_ADMIN, User.Role.ADMIN],
        login_url=login_url,
        redirect_field_name=redirect_field_name
        
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
