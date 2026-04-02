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
        # 🔹 ADMIN: barcha userlar
        users = User.objects.all()

        # Har bir user uchun mashinalar va oxirgi ish
        for u in users:
            u.cars_list = u.cars.all()
            if model_filter:
                u.cars_list = u.cars_list.filter(model=model_filter)
            if query:
                u.cars_list = u.cars_list.filter(
                    Q(model__icontains=query) |
                    Q(plate_number__icontains=query)
                )
            # Har bir mashina uchun oxirgi ish
            for car in u.cars_list:
                last_payment = Payment.objects.filter(car=car).order_by('-created_at').first()
                car.last_description = last_payment.description if last_payment else "Ish yozilmagan"

        fund = Fund.objects.first()
        context = {
            'users': users,
            'fund': fund,
            'query': query,
            'model_filter': model_filter,
            'models_list': Car.objects.values_list('model', flat=True).distinct(),
        }

    else:
        # 🔹 ODDIY USER
        cars = user.cars.all()
        payments = user.payments.all().order_by('-created_at')
        context = {
            'cars': cars,
            'payments': payments,
        }

    return render(request, 'dashboard.html', context)