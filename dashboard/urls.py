from django.urls import path
from .views import dashboard_view, splash_view

urlpatterns = [

    # 🔥 SPLASH
    path('', splash_view, name='splash'),

    # 🏠 DASHBOARD
    path('dashboard/', dashboard_view, name='dashboard'),

]