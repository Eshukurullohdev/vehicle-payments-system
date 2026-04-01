from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # register qilgandan so'ng avtomatik login
            return redirect('dashboard')  # <-- shu yer dashboardga yo'naltiradi
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # logindan keyin dashboardga yo'naltirish
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