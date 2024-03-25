from django.db import models
from vehicle.models import Vehicle
# import json
# Create your models here.
class FullInsurance(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='full_insurances')
    insurer = models.CharField(max_length=255, null=True,blank=True)
    issue_date = models.DateField(null=True,blank=True)
    expire_date = models.DateField(null=True,blank=True)
    notification_status = models.BooleanField(default=False)
    images = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def set_images(self, image_list):
    #     self.images = json.dumps(image_list)

    # def get_images(self):
    #     return json.loads(self.images) if self.images else []