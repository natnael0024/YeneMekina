from django.db import models
from vehicle.models import Vehicle
import os
import uuid
# Create your models here.

class RoadFund(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='road_funds')
    issue_date = models.DateField(null=True, blank=True)
    expire_date = models.DateField(null=True,blank=True)
    image = models.ImageField(upload_to='roadfunds/',null=True,blank=True)
    notification_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

