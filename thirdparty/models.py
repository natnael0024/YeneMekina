from django.db import models
from vehicle.models import Vehicle

# Create your models here.
class ThirdParty(models.Model):
    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE, related_name='third_parties')
    insurer = models.CharField(max_length=255,null=True,blank=True)
    issue_date = models.DateField(null=True,blank=True)
    expire_date = models.DateField(null=True,blank=True)
    image = models.ImageField(upload_to='thidparties/',null=True,blank=True)
    notification_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
