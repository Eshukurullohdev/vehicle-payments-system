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