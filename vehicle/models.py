from django.db import models
from accounts.models import CustomUser

class Vehicle(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, null=True)
    model = models.CharField(max_length=255, null=True)
    image = models.TextField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

