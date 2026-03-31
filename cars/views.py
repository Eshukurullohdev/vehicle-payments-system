from django.shortcuts import render

from django.shortcuts import render, redirect
from .forms import CarForm
from django.contrib.auth.decorators import login_required

@login_required
def add_car_view(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.user = request.user
            car.save()
            return redirect('dashboard')
    else:
        form = CarForm()
    return render(request, 'cars/add_car.html', {'form': form})
