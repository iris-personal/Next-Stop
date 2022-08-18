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
    accommodation = models.CharField(max_length=100, default='None Yet!')
    notes = models.CharField(max_length=1000, default='None Yet!')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'trip_id': self.id})

class Activity(models.Model):
    a_time = models.TimeField('Activity Time')
    a_date = models.DateField('Activity Date')
    activity = models.CharField(max_length=100)
    notes = models.CharField(max_length=1000)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_activity_display()} on {self.a_date}'
    
    class Meta:
        ordering = ['a_date']
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'trip_id': self.trip.id})
