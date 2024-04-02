from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Map(models.Model):
      name=models.CharField(max_length=100)
      lat=models.FloatField(max_length=100)
      lon=models.FloatField(max_length=100)
      type=models.CharField(max_length=100)
      city=models.CharField(max_length=100)
      country=models.CharField(max_length=100)
      phone = models.CharField(max_length=255)
      email = models.EmailField()

      def __str__(self):
           return self.name
     