from django import forms
from .models import Car
from django.contrib.auth import get_user_model

User = get_user_model()

class CarForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    # 🔥 Car fieldlar
    car_model = forms.CharField(max_length=100)
    car_year = forms.IntegerField()
    plate_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['phone', 'password']