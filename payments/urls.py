from django.urls import path
from .views import add_payment_view

urlpatterns = [
    path('add/', add_payment_view, name='add_payment'),
]