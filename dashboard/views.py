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

from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


def clean_phone(value):
    if not value:
        return ""
    return value.replace(" ", "").replace("+", "")

@login_required
def dashboard_view(request):
    user = request.user

    query = request.GET.get('q', '').strip()
    model_filter = request.GET.get('model', '')

    # 🔥 ENG OXIRGI ADMIN
    admin_user = User.objects.filter(
        is_staff=True
    ).order_by('-id').first()

    if user.is_staff:

        users = User.objects.filter(
            is_staff=False
        ).order_by('-id')

        if query or model_filter:

            cars = Car.objects.select_related('user').filter(
                user__is_staff=False
            )

            if query:
                cars = cars.filter(
                    Q(user__phone__icontains=query) |
                    Q(user__phone__endswith=query) |
                    Q(model__icontains=query) |
                    Q(plate_number__icontains=query)
                )

            if model_filter:
                cars = cars.filter(model=model_filter)

            users_dict = {}

            for car in cars:
                users_dict.setdefault(car.user, []).append(car)

            users = []

            for u, cars_list in users_dict.items():
                u.cars_list = cars_list
                users.append(u)

        else:

            for u in users:
                u.cars_list = list(u.cars.all())

        fund = Fund.objects.first()

        return render(request, 'dashboard.html', {
            'users': users,
            'fund': fund,
            'query': query,
            'model_filter': model_filter,
            'admin_user': admin_user,
            'models_list': Car.objects.values_list(
                'model',
                flat=True
            ).distinct(),
        })

    else:

        cars = user.cars.all()

        payments = user.payments.all().order_by('-created_at')

        fund = Fund.objects.first()

        return render(request, 'dashboard.html', {
            'cars': cars,
            'payments': payments,
            'fund': fund,
            'admin_user': admin_user,  # 🔥 USERLARGA HAM YUBORILYAPTI
        })

def splash_view(request):
    return render(request, 'splash.html')