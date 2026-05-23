from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Telefon raqam bo‘lishi kerak")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from decimal import Decimal

class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=20, unique=True)

    # 🔥 USER RAQAMI
    user_number = models.PositiveIntegerField(
        unique=True,
        null=True,
        blank=True
    )



    cashback_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    full_name = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    last_seen = models.DateTimeField(null=True, blank=True)
    can_chat = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

def save(self, *args, **kwargs):

    # 🔥 faqat oddiy userlarga raqam
    if not self.user_number and not self.is_staff:

        existing_numbers = User.objects.filter(
            is_staff=False
        ).values_list(
            'user_number',
            flat=True
        )

        existing_numbers = sorted([
            n for n in existing_numbers if n
        ])

        next_number = 1

        for number in existing_numbers:

            if number == next_number:
                next_number += 1
            else:
                break

        self.user_number = next_number

    super().save(*args, **kwargs)

    def add_cashback(self, amount):
        self.cashback_balance += Decimal(amount)
        self.save()

    def __str__(self):
        return f"{self.user_number} - {self.phone}"


from django.db import models

class Product(models.Model):
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    description = models.TextField(blank=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0,
    validators=[MinValueValidator(0)]
)
    is_sold = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name