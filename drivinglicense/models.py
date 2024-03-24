from django.db import models
from accounts.models import CustomUser
import os
import uuid
from datetime import datetime
# Create your models here.

class DrivingLicense(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='driving_licenses')
    license_number =  models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expire_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='licenses/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Check if the image field is not empty
        if self.image:
            # Extract the original file extension
            file_extension = os.path.splitext(self.image.name)[1]
            # Generate a unique file name with the original file name and UUID
            file_name = f'license_{uuid.uuid4()}{file_extension}'
            # Update the image field with the new file name
            self.image.name = f'{file_name}'
        super(DrivingLicense, self).save(*args, **kwargs)