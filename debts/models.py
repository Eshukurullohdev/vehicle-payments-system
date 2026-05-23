from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Debt(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_debts')
    created_at = models.DateTimeField(auto_now_add=True)

    def display_name(self):
        if self.user:
            return self.user.phone
        return self.name or self.phone