from django.db import models

# Create your models here. 
class Advert(models.Model):
    title=models.CharField(max_length=200)
    desc=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    priority=models.CharField(max_length=200)
    price=models.FloatField(max_length=200)
    expire_date=models.DateTimeField(null=True, blank=True)
    image=models.ImageField(upload_to='advert/images',null=True)

