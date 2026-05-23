from django.urls import path
from .views import add_car_view

urlpatterns = [
    path('add/', add_car_view, name='add_car'),
]