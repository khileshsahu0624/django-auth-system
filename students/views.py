import random
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import admin_required
from .models import Student
from .forms import StudentForm

User = get_user_model()

# ========== LOGIN (OTP Generation) ==========
def user_login(request):
    if request.user.is_authenticated:
        return redirect('student_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        
        try:
            user = User.objects.get(username=username)
            # Generate 6 digit OTP
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.otp_created_at = timezone.now()
            user.save()

            # Print to console for development
            print(f"\n{'='*40}")
            print(f"OTP for {user.username}: {otp}")
            print(f"{'='*40}\n")

            # Store username in session for verification step
            request.session['auth_username'] = username
            messages.success(request, 'An OTP has been sent. Please check the terminal console.')
            return redirect('verify_otp')
        except User.DoesNotExist:
            messages.error(request, 'User with that username does not exist.')

    return render(request, 'students/login.html')

# ========== VERIFY OTP ==========
def verify_otp(request):
    if request.user.is_authenticated:
        return redirect('student_list')
        
    username = request.session.get('auth_username')
    if not username:
        messages.error(request, 'Session expired or invalid. Please try logging in again.')
        return redirect('login')

    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        try:
            user = User.objects.get(username=username)
            
            # Check if OTP matches and is within 5 minutes
            if user.otp == otp_entered:
                time_diff = timezone.now() - user.otp_created_at
                if time_diff.total_seconds() <= 300: # 5 minutes
                    # OTP is valid
                    # We can log the user in directly (bypassing password) since we verified OTP
                    # We must specify the backend since authenticate wasn't called
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    
                    # Clear OTP
                    user.otp = None
                    user.otp_created_at = None
                    user.save()
                    
                    # Clear session
                    del request.session['auth_username']
                    
                    messages.success(request, 'Login successful!')
                    return redirect('student_list')
                else:
                    messages.error(request, 'OTP has expired. Please try logging in again.')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('login')

    return render(request, 'students/verify_otp.html')

# ========== LOGOUT ==========
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

# ========== STUDENT LIST (Read) ==========
@login_required(login_url='login')
def student_list(request):
    students = Student.objects.all().order_by('-created_at')
    return render(request, 'students/student_list.html', {'students': students})

# ========== CREATE ==========
@admin_required(login_url='login')
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Add Student'})

# ========== UPDATE ==========
@admin_required(login_url='login')
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Edit Student'})

# ========== DELETE ==========
@admin_required(login_url='login')
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})