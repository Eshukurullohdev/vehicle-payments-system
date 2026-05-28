from django import forms
from .models import User


CAR_MODELS = [
    # 🇺🇿 UzAuto
    ("Nexia 1", "Chevrolet Nexia 1"),
    ("Nexia 2", "Chevrolet Nexia 2"),
    ("Nexia 3", "Chevrolet Nexia 3"),
    ("Matiz", "Chevrolet Matiz"),
    ("Cobalt", "Chevrolet Cobalt"),
    ("Lacetti", "Chevrolet Lacetti"),
    ("Onix", "Chevrolet Onix"),
    ("Tracker", "Chevrolet Tracker"),
    ("Damas", "Chevrolet Damas"),
    ("Malibu", "Chevrolet Malibu"),

    # 🇨🇳 Chinese (UZda mashhur)
    ("BYD Song Plus", "BYD Song Plus"),
    ("BYD Qin Plus", "BYD Qin Plus"),
    ("BYD Han", "BYD Han"),
    ("BYD Dolphin", "BYD Dolphin"),

    ("Chery Tiggo 7", "Chery Tiggo 7"),
    ("Chery Tiggo 8", "Chery Tiggo 8"),
    ("Haval H6", "Haval H6"),
    ("Haval Jolion", "Haval Jolion"),
    ("Geely Monjaro", "Geely Monjaro"),

    # 🇰🇷 Korea
    ("Kia K5", "Kia K5"),
    ("Kia Sportage", "Kia Sportage"),
    ("Hyundai Elantra", "Hyundai Elantra"),
    ("Hyundai Tucson", "Hyundai Tucson"),

    # 🇯🇵 Japan
    ("Toyota Camry", "Toyota Camry"),
    ("Toyota Corolla", "Toyota Corolla"),
    ("Toyota Land Cruiser", "Toyota Land Cruiser"),

    # 🇩🇪 Germany
    ("BMW 5 Series", "BMW 5 Series"),
    ("Mercedes E Class", "Mercedes E Class"),
]
YEAR_CHOICES = [
    (year, year) for year in range(2026, 1980, -1)
]

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "••••••••"
        })
    )

    car_model = forms.ChoiceField(
        choices=CAR_MODELS,
        label="Mashina modeli",
        widget=forms.Select(attrs={
            "placeholder": "Mashina modelini tanlang"
        })
    )

    car_year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        label="Yili",
        widget=forms.Select(attrs={
            "placeholder": "2020"
        })
    )

    plate_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "placeholder": "01 A 777 AA"
        })
    )

    class Meta:
        model = User
        fields = ['phone', 'password']
        widgets = {
            "phone": forms.TextInput(attrs={
                "placeholder": "+998 90 123 45 67"
            })
        }

from .models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'phone', 'profile_image']  # foydalanuvchi o‘z profilini yangilashi uchun kerakli maydonlar