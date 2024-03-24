from django.db import models
from vehicle.models import Vehicle
import uuid
import os

class Bolo(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bolos')
    inspection_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='bolos/', blank=True, null=True)
    notification_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self._original_image = self.image.name

    # def save(self, *args, **kwargs):
    #     if self.image :
    #         file_extension = os.path.splitext(self.image.name)[1]
    #         self.image.name = f'bolo_{uuid.uuid4()}{file_extension}'
    #     super(Bolo, self).save(*args, **kwargs)