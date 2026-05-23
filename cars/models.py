from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    plate_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.model} ({self.plate_number})"