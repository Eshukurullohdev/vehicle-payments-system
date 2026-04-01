from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=20, unique=True)
    cashback_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    full_name = models.CharField(max_length=100, blank=True, null=True)  # 👤
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)  # 🖼
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def add_cashback(self, amount):
        self.cashback_balance += Decimal(amount)
        self.save()

    def __str__(self):
        return self.phone