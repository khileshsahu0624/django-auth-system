from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from accounts.decorators import admin_required

User = get_user_model()

@login_required(login_url='login')
@admin_required(login_url='login')
def users_roles_view(request):
    users = User.objects.all().order_by('-date_joined')
    roles = User.Role.choices
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        if user_id and new_role:
            try:
                target_user = User.objects.get(id=user_id)
                target_user.role = new_role
                target_user.save()
                messages.success(request, f"Successfully updated role for {target_user.username}.")
                return redirect('users_roles')
            except User.DoesNotExist:
                messages.error(request, "User not found.")
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    active_percentage = round((active_users / total_users) * 100, 1) if total_users > 0 else 0
                
    context = {
        'users': users, 
        'roles': roles,
        'total_users': total_users,
        'active_users': active_users,
        'active_percentage': active_percentage,
        'roles_count': len(roles)
    }
    return render(request, 'students/users_roles.html', context)
