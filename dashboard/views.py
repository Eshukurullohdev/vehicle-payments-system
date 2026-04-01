from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cars.models import Car
from payments.models import Payment, Fund
from django.db.models import Q

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cars.models import Car
from payments.models import Payment, Fund
from django.db.models import Q
from collections import defaultdict
from users.models import User

from django.shortcuts import render
from cars.models import Car
from payments.models import Payment, Fund
from django.db.models import Q

@login_required
def dashboard_view(request):
    user = request.user
    query = request.GET.get('q', '')
    model_filter = request.GET.get('model', '')

    if user.is_staff:
        # Admin uchun userlar ro'yxati
        users = User.objects.all()

        # Har bir userga mashinalar ro'yxatini qo'shamiz
        for u in users:
            u.cars_list = u.cars.all()
            if model_filter:
                u.cars_list = u.cars_list.filter(model=model_filter)
            if query:
                u.cars_list = u.cars_list.filter(
                    Q(model__icontains=query) |
                    Q(plate_number__icontains=query)
                )

        # Car payments (filter qo'llash mumkin)
        car_payments = []
        cars = Car.objects.all()
        if model_filter:
            cars = cars.filter(model=model_filter)
        if query:
            cars = cars.filter(
                Q(model__icontains=query) |
                Q(plate_number__icontains=query) |
                Q(user__phone__endswith=query)
            )
        for car in cars:
            payments = Payment.objects.filter(user=car.user)
            total_paid = sum(p.amount for p in payments)
            total_cashback = sum(p.cashback for p in payments)
            last_payment = payments.order_by('-created_at').first()
            car_payments.append({
                'car': car,
                'owner': car.user,
                'total_paid': total_paid,
                'total_cashback': total_cashback,
                'last_payment': last_payment,
            })

        fund = Fund.objects.first()

        context = {
            'users': users,
            'car_payments': car_payments,
            'fund': fund,
            'query': query,
            'model_filter': model_filter,
            'models_list': Car.objects.values_list('model', flat=True).distinct(),
        }
    else:
        # Oddiy user
        cars = user.cars.all()
        payments = user.payments.all()
        context = {
            'cars': cars,
            'payments': payments,
        }

    return render(request, 'dashboard.html', context)