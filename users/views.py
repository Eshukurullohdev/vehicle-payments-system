from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm
from decimal import Decimal, InvalidOperation
from cars.models import Car
import random
def safe_decimal(value):
    try:
        if not value:
            return Decimal("0")

        value = str(value).replace(" ", "").replace(",", "")
        return Decimal(value)

    except (InvalidOperation, TypeError):
        return Decimal("0")

def register_view(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():

            # 📱 phone olish
            phone = normalize_phone(form.cleaned_data['phone'])
            password = form.cleaned_data['password']

            # 👤 USER CREATE (ENG TO‘G‘RI YO‘L)
            user = User.objects.create_user(
                phone=phone,
                password=password
            )

            # 🚗 CAR CREATE
            Car.objects.create(
                user=user,
                model=form.cleaned_data['car_model'],
                year=form.cleaned_data['car_year'],
                plate_number=form.cleaned_data['plate_number']
            )

            login(request, user)
            return redirect('dashboard')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .utils import normalize_phone




def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        phone = normalize_phone(phone)  # 🔥 ENG MUHIM

        user = User.objects.filter(phone=phone).first()

        if user and user.check_password(password):
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Telefon yoki parol noto‘g‘ri"
            return render(request, 'users/login.html', {'error': error})

    return render(request, 'users/login.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserUpdateForm

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)  # <--- request.FILES
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from collections import defaultdict

User = get_user_model()

@login_required
def admin_user_detail(request, user_id):
    # Faqat adminga ruxsat
    if not request.user.is_staff:
        return redirect('dashboard')

    # User va unga tegishli ma’lumotlar
    user = get_object_or_404(User, id=user_id)
    cars = user.cars.all()
    payments = user.payments.all().order_by('created_at')

    # Cashback history chart data
    history = defaultdict(float)
    for p in payments:
        date = p.created_at.strftime("%Y-%m-%d")
        history[date] += float(p.cashback)

    context = {
        'user': user,
        'cars': cars,
        'payments': payments,
        'history_labels': list(history.keys()),
        'history_data': list(history.values()),
    }

    return render(request, 'users/admin_user_detail.html', context)



@login_required
def admin_users_dashboard(request):
    # Faqat admin kirishi mumkin
    if not request.user.is_staff:
        return redirect('dashboard')

    users = User.objects.all().order_by('-id')  # barcha userlar
    context = {
        'users': users
    }
    return render(request, 'dashboard_admin_users.html', context)


from django.shortcuts import render
from .models import Product

def safe_decimal(value):
    try:
        if not value:
            return Decimal("0")

        value = str(value).replace(" ", "").replace(",", "")
        return Decimal(value)
    except (InvalidOperation, AttributeError):
        return Decimal("0")


# 📦 PRODUCT LIST
def product_list(request):

    category = request.GET.get('category')

    products = Product.objects.all().order_by('-id')

    if category:
        products = products.filter(category=category)

    return render(request, 'users/list.html', {
        'products': products,
        'category': category
    })


# ➕ ADD PRODUCT
@staff_member_required
@staff_member_required
def add_product(request):

    if request.method == "POST":

        Product.objects.create(
            name=request.POST.get('name'),
            price=safe_decimal(request.POST.get('price')),
            phone=request.POST.get('phone'),
            image=request.FILES.get('image'),
            category=request.POST.get('category'),  # 🔥 MUHIM
            description=request.POST.get('description')
        )

        return redirect('products')

    return render(request, 'users/add.html')

# ✏️ EDIT PRODUCT
@staff_member_required
def edit_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == "POST":
        product.name = request.POST.get('name')
        product.phone = request.POST.get('phone')

        # 🔥 FIXED PRICE
        product.price = safe_decimal(request.POST.get('price'))

        product.is_sold = request.POST.get('is_sold') == 'on'

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()
        return redirect('products')

    return render(request, 'users/edit.html', {
        'product': product
    })


# 🔥 TOGGLE SOLD (AJAX)
@staff_member_required
def toggle_sold(request, pk):
    product = get_object_or_404(Product, id=pk)
    product.is_sold = not product.is_sold
    product.save()

    return JsonResponse({
        "success": True,
        "is_sold": product.is_sold
    })


# 🗑 DELETE PRODUCT (AJAX)
@staff_member_required
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    product.delete()

    return JsonResponse({
        "success": True
    })


@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # ❗ admin o‘zini o‘chirmasin
    if user == request.user:
        return redirect('dashboard')

    user.delete()
    return redirect('dashboard')


@login_required
def admin_random_users(request):

    # 🔒 faqat admin
    if not request.user.is_staff:
        return redirect('dashboard')

    users = list(User.objects.filter(is_staff=False))

    # 🔀 random qilish
    random.shuffle(users)

    # 📌 display number berish (faqat UI uchun)
    for i, user in enumerate(users, start=1):
        user.temp_number = i

    return render(request, 'users/admin_random_users.html', {
        'users': users
    })

@login_required
def random_user_picker(request):

    if not request.user.is_staff:
        return redirect('dashboard')

    winner = None

    if request.method == "POST":
        users = list(User.objects.filter(is_staff=False))

        if users:
            winner = random.choice(users)

    return render(request, 'users/random_picker.html', {
        'winner': winner
    })