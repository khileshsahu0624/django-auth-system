from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserForm

User = get_user_model()

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'user_management/user_list.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        context['total_users'] = total_users
        context['active_users'] = active_users
        context['active_percentage'] = round((active_users / total_users) * 100, 1) if total_users > 0 else 0
        from .models import Role
        context['roles'] = Role.objects.all()
        context['roles_count'] = Role.objects.count()
        return context

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        new_role_id = request.POST.get('role')
        if user_id and new_role_id:
            try:
                target_user = User.objects.get(id=user_id)
                from .models import Role
                target_user.role = Role.objects.get(id=new_role_id)
                target_user.save()
                messages.success(request, f"Successfully updated role for {target_user.username}.")
            except (User.DoesNotExist, Role.DoesNotExist):
                messages.error(request, "User or Role not found.")
        return redirect('users_roles')

class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'user_management/user_form.html'
    success_url = reverse_lazy('users_roles')

    def form_valid(self, form):
        messages.success(self.request, "User created successfully.")
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user_management/user_form.html'
    success_url = reverse_lazy('users_roles')

    def form_valid(self, form):
        messages.success(self.request, "User updated successfully.")
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'user_management/user_confirm_delete.html'
    success_url = reverse_lazy('users_roles')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False # Soft delete
        user.save()
        messages.success(request, f"User {user.username} has been deactivated.")
        return redirect(self.success_url)

from .models import Role

class RoleListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Role
    template_name = 'user_management/role_list.html'
    context_object_name = 'roles'
    
class RoleCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Role
    fields = ['name', 'description', 'permissions']
    template_name = 'user_management/role_form.html'
    success_url = reverse_lazy('role_list')

    def form_valid(self, form):
        messages.success(self.request, "Role created successfully.")
        return super().form_valid(form)

class RoleUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Role
    fields = ['name', 'description', 'permissions']
    template_name = 'user_management/role_form.html'
    success_url = reverse_lazy('role_list')

    def form_valid(self, form):
        messages.success(self.request, "Role updated successfully.")
        return super().form_valid(form)

class RoleDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Role
    template_name = 'user_management/role_confirm_delete.html'
    success_url = reverse_lazy('role_list')

    def delete(self, request, *args, **kwargs):
        role = self.get_object()
        messages.success(request, f"Role {role.name} has been deleted.")
        return super().delete(request, *args, **kwargs)
