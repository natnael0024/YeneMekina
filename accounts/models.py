

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass
    phone_number = models.CharField(max_length=255, unique=True) # Set unique=False for no
    lang = models.CharField(max_length=2, default='am')
    avatar = models.CharField(max_length=255, null=True, blank=True) 
    otp = models.CharField(max_length=255, null=True, blank=True)
    otp_timestamp = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=255, default='active')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
   