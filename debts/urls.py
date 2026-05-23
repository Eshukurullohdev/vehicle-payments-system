from django.urls import path
from .views import *

app_name = 'debts'

urlpatterns = [
    path('', admin_debts, name='admin_debts'),
    path('reduce/<int:pk>/', reduce_debt, name='reduce_debt'),
    path('delete/<int:pk>/', delete_debt, name='delete_debt'),
]