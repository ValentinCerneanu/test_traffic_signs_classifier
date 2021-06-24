from django.db import models

# Create your models here.
class TrafficSign(models.Model):
    name = models.CharField(max_length=50)
    car = models.ImageField(upload_to='images/')