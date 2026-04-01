from django import forms
from .models import User

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['phone', 'password']


from .models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'phone', 'profile_image']  # foydalanuvchi o‘z profilini yangilashi uchun kerakli maydonlar