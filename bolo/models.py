from django.db import models
from django.contrib.auth.models import User
from vehicle.models import Vehicle

class Bolo(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bolos')
    inspection_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='bolos/', blank=True, null=True)
    notification_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f"{self.vehicle.plate_number} - Bolo"