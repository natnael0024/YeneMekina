from django.db import models
from accounts.models import CustomUser

class Document(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='documents')
    images = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)