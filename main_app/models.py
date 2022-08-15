from unicodedata import name
from django.db import models
from django.urls import reverse
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

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'trip_id': self.id})

class Activity(models.Model):
    d_time = models.DateTimeField('Activity Day')
    activity = models.CharField(max_length=100)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_activity_display()} on {self.d_time}'
    
    class Meta:
        ordering = ['d_time']
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'trip_id': self.trip.id})

class Destination(models.Model):
    destination_type = models.CharField(max_length= 100)
    name = models.CharField(max_length= 100)
    walk_score_url = models.CharField(max_length= 100)
    budget = models.CharField(max_length= 100)
    safety = models.CharField(max_length= 100)
    known_for = models.CharField(max_length= 100)
    photos = models.CharField(max_length= 100)