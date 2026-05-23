from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from .models import Debt

User = get_user_model()


@staff_member_required
def admin_debts(request):
    users = User.objects.all()

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        amount = request.POST.get("amount")
        description = request.POST.get("description")

        user = None
        if user_id:
            user = User.objects.get(id=user_id)

        Debt.objects.create(
            user=user,
            name=name,
            phone=phone,
            amount=Decimal(amount),
            description=description,
            created_by=request.user
        )

        return redirect('debts:admin_debts')

    debts = Debt.objects.all().order_by('-created_at')

    return render(request, 'debts/admin.html', {
        'debts': debts,
        'users': users
    })


def reduce_debt(request, pk):
    debt = get_object_or_404(Debt, id=pk)

    if request.method == "POST":
        amount = Decimal(request.POST.get("amount", "0"))

        if amount > 0:
            debt.amount -= amount

            if debt.amount <= 0:
                debt.amount = 0

            debt.save()

    return redirect('debts:admin_debts')


def delete_debt(request, pk):
    debt = get_object_or_404(Debt, id=pk)
    debt.delete()
    return redirect('debts:admin_debts')