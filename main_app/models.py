from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Trip(models.Model):
    name = models.CharField(max_length=40)
    destinations = models.CharField(max_length=80)
    start = models.DateField('Start Date')
    end = models.DateField('End Date')
    accommodation = models.CharField(max_length=100)
    journal = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)