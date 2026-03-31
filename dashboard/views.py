from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cars.models import Car
from payments.models import Payment, Fund
from django.db.models import Q

@login_required
def dashboard_view(request):
    user = request.user
    query = request.GET.get('q', '')  # search query
    model_filter = request.GET.get('model', '')  # filter dropdown

    if user.is_staff:
        cars = Car.objects.all().order_by('user__phone')
        car_payments = []

        # Dropdown uchun barcha unique mashina modellari
        models_list = Car.objects.values_list('model', flat=True).distinct()

        for car in cars:
            # Filter by model
            if model_filter and car.model != model_filter:
                continue

            # User telefon oxirgi 4 raqam bilan filter
            if query and query.isdigit() and len(query) <= 4:
                if not str(car.user.phone).endswith(query):
                    continue

            # Mashina modeli yoki plate bilan filter
            if query and not (query.isdigit() and len(query) <= 4):
                if query.lower() not in car.model.lower() and query.lower() not in car.plate_number.lower():
                    continue

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
            'car_payments': car_payments,
            'fund': fund,
            'query': query,
            'models_list': models_list,
            'model_filter': model_filter,
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