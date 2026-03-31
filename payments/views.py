from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm
from .models import Payment

@login_required
def add_payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            if request.user.is_staff and form.cleaned_data.get('car'):
                # Admin mashina tanladi
                payment.user = form.cleaned_data['car'].user
            else:
                # Oddiy user
                payment.user = request.user

            payment.save()
            return redirect('dashboard')
    else:
        form = PaymentForm()
    return render(request, 'payments/add_payment.html', {'form': form})