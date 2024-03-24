from django.db import models
from django.contrib.auth.models import User
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


    def save(self, *args, **kwargs):
        # Check if the image field is not empty
        if self.image:
            # Extract the original file extension
            file_extension = os.path.splitext(self.image.name)[1]
            # Generate a unique file name with the original file name and UUID
            file_name = f'bolo_{uuid.uuid4()}{file_extension}'
            # Update the image field with the new file name
            self.image.name = f'{file_name}'
        super(Bolo, self).save(*args, **kwargs)