from django import forms
from .models import Payment
from cars.models import Car

class PaymentForm(forms.ModelForm):
    # Admin uchun mashina tanlash qo‘shamiz
    car = forms.ModelChoiceField(queryset=Car.objects.all(), required=False)

    class Meta:
        model = Payment
        fields = ['amount', 'car', 'description']  # description maydonini qo‘shamiz