from django.db import models

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

from decimal import Decimal

from django.conf import settings
from django.apps import apps
from .utils import calculate_cashback

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cashback = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Cashback hisoblash
        self.cashback = calculate_cashback(self.amount)

        super().save(*args, **kwargs)  # Payment saqlanadi

        # User cashback balansi update
        user = self.user
        user.add_cashback(self.cashback)

        # Jamg‘arma update
        FundModel = apps.get_model('payments', 'Fund')
        fund, created = FundModel.objects.get_or_create(id=1)
        fund.add_amount(self.cashback)


from decimal import Decimal
from django.db import models
from django.conf import settings
from django.apps import apps
from .utils import calculate_cashback

User = settings.AUTH_USER_MODEL


class Fund(models.Model):
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def add_amount(self, amount):
        self.total_amount += Decimal(amount)
        self.save()

    def __str__(self):
        return f"Fund: {self.total_amount}"

from django.db import models
from django.contrib.auth import get_user_model
from django.apps import apps

User = get_user_model()

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    cashback = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        from decimal import Decimal

        is_new = self.pk is None

        self.cashback = calculate_cashback(self.amount)

        super().save(*args, **kwargs)

        if is_new:
            user = self.user
            user.add_cashback(self.cashback)

            FundModel = apps.get_model('payments', 'Fund')
            fund, _ = FundModel.objects.get_or_create(id=1)
            fund.add_amount(self.cashback)


class PaymentRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('approved', 'Tasdiqlandi'),
        ('rejected', 'Rad etildi'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_requests')
    screenshot = models.ImageField(upload_to='checks/')
    amount = models.IntegerField(default=49000)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.status}"


# payments/models.py

class CashbackWithdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.PositiveIntegerField()
    description = models.CharField(max_length=255, default="Cashback yechib olindi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount}"