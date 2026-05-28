from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm
from .models import Payment
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from .models import CashbackWithdraw
User = get_user_model()
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

from .models import PaymentRequest

@login_required
def send_payment_request(request):
    if request.method == 'POST':
        screenshot = request.FILES.get('screenshot')

        PaymentRequest.objects.create(
            user=request.user,
            screenshot=screenshot
        )

        return redirect('dashboard')

    return render(request, 'payments/send_check.html')

@login_required
def admin_payment_requests(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    requests = PaymentRequest.objects.all().order_by('-created_at')

    return render(request, 'payments/admin_requests.html', {
        'requests': requests
    })


@login_required
def approve_payment(request, pk):
    if not request.user.is_staff:
        return redirect('dashboard')

    payment = PaymentRequest.objects.get(id=pk)

    if payment.status == 'pending':
        payment.status = 'approved'
        payment.save()

        user = payment.user

        # 🔥 5% cashback
        cashback = payment.amount * Decimal('0.05')

        user.cashback_balance += cashback
        user.can_chat = True
        user.save()

    return redirect('payments:admin_requests')

@login_required
def chat_view(request):
    if not request.user.can_chat:
        return redirect('send_payment_request')

    return render(request, 'chat.html')

# payments/views.py

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def withdraw_cashback(request):
    users = User.objects.all()

    if request.method == "POST":
        user_id = request.POST.get('user_id')
        amount = int(request.POST.get('amount'))

        user = User.objects.get(id=user_id)

        if user.cashback_balance >= amount:
            user.cashback_balance -= amount
            user.save()

            CashbackWithdraw.objects.create(
                user=user,
                amount=amount
            )

        return redirect('dashboard')

    return render(request, 'payments/withdraw.html', {
        'users': users
    })