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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self._original_image = self.image.name

    # def save(self, *args, **kwargs):
    #     if self.image and self.image.name != self._original_image:
    #         file_extension = os.path.splitext(self.image.name)[1]
    #         self.image.name = f'license_{uuid.uuid4()}{file_extension}'
    #     super(DrivingLicense, self).save(*args, **kwargs)