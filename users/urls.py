from django.urls import path
from .views import *
from django.contrib.auth.views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
     path('profile/', profile_view, name='profile'),

    path('password-change/', 
         PasswordChangeView.as_view(template_name='users/password_change.html'), 
         name='password_change'),

    path('password-change/done/', 
         PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), 
         name='password_change_done'),
  
     path('admin/user/<int:user_id>/', admin_user_detail, name='admin_user_detail'),
     path('admin/users/', admin_users_dashboard, name='admin_users_dashboard'),
]