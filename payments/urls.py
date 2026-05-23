from django.urls import path
from .views import *
app_name = 'payments'
urlpatterns = [
    path('add/', add_payment_view, name='add_payment'),
    path('send-payment/', send_payment_request, name='send_payment_request'),
    path('admin-requests/', admin_payment_requests, name='admin_requests'),
    path('approve/<int:pk>/', approve_payment, name='approve_payment'),
    path('withdraw/', withdraw_cashback, name='withdraw_cashback'),
]