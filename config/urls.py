from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('cars/', include('cars.urls')),
    path('payments/', include('payments.urls')),
    path('', include('dashboard.urls')),
]
