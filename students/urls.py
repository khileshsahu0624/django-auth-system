from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='register_ui'),
    path('login/', views.user_login, name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('logout/', views.user_logout, name='logout'),

    path('', views.landing_page, name='landing'),
    path('dashboard/', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('update/<int:pk>/', views.student_update, name='student_update'),
    path('delete/<int:pk>/', views.student_delete, name='student_delete'),
    
    # NOTE: The "Users & Roles" dashboard is NOT managed by this 'students' app anymore.
    # It has been moved to its own dedicated app called 'user_management'.
    # The URL for it is defined in: user_management/urls.py (name='users_roles')
    # and it is connected to the main project via student_project/urls.py under the path 'management/'.
    # Because of this, you just need to use {% url 'users_roles' %} in your HTML, and Django will automatically
    # find it in the user_management app. You DO NOT need to write a URL or View for it here in the students app!
]