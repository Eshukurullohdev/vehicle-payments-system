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
     path('products/', product_list, name='products'),
     path('products/add/', add_product, name='add_product'),
     path('products/edit/<int:pk>/', edit_product, name='edit_product'),
     path('products/toggle/<int:pk>/', toggle_sold, name='toggle_sold'),
     path('products/delete/<int:pk>/', delete_product, name='delete_product'),
     path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
     path('random-users/', admin_random_users, name='admin_random_users'),
     path('random-picker/', random_user_picker, name='random_picker'),
]