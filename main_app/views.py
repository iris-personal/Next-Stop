from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from .models import Trip, Activity, Destination
from .forms import ActivityForm
import requests
import os
import http.client
import base64
import random


# Create your views here.
def home(request):
  return render(request, 'home.html')

@login_required
def trips_index(request):
  trips = Trip.objects.filter(user=request.user)
  return render(request, 'trips/index.html', {'trips' : trips})

@login_required
def trips_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    activity_form = ActivityForm()
    return render(request, 'trips/detail.html', {
      'trip': trip,
      'activity_form': activity_form,
    })


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      #this will add the user to the DB
      user = form.save()
      # auto matically log in the new user 
      login(request, user)
      return redirect('index')
  else: 
    error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def add_activity(request, trip_id):
  form = ActivityForm(request.POST)
  if form.is_valid():
    new_activity = form.save(commit=False)
    new_activity.trip_id = trip_id
    new_activity.save()
  return redirect('detail', trip_id=trip_id)

def destinations(request):
  return render(request, 'destinations.html')

def destinations_search(request):
  cityId = random.randint(6576468, 10936014)
  # print(cityId)
  secret_key = os.environ['SECRET_KEY']
  access_key = os.environ['ACCESS_KEY']
  encoded_bytes = base64.b64encode(f'{access_key}:{secret_key}'.encode("utf-8"))
  auth_key = str(encoded_bytes, "utf-8")
  headers = {
    'Authorization': f'Basic {auth_key}'
  }
  response = requests.get(f'https://api.roadgoat.com/api/v2/destinations/7879186', headers=headers)
  data = response.json()
  budget = data['data']['attributes']['budget']
  budgetText = budget[(list(budget.keys())[0])]
  text = budgetText['subText']
  safety = data['data']['attributes']['safety']
  safetyText = safety[(list(safety.keys())[0])] 
  safetyRating = safetyText['subText']
  covid = data['data']['attributes']['covid']
  covidText = covid[(list(covid.keys())[0])]
  covidRating = covidText['text']
  avgRating = data["data"]["attributes"]["average_rating"]
  avgRatingCond = "{:.2f}".format(avgRating)
  photo = data['included'][1]['attributes']['image']['thumb']
  slugs = []
  # known_for = data['included']
  for item in data['included']:
    if item['type'] == 'known_for':
      slugs.append(item['attributes']['slug'])
 
 
  return render(request, 'destinations.html', {
   'data': data,
   'text': text,
   'safetyRating': safetyRating,
   'covidRating': covidRating,
   'photo': photo,
   'slugs': slugs,
   'avgRatingCond': avgRatingCond
  })

class TripsCreate(LoginRequiredMixin, CreateView):
  model = Trip
  fields = ['name', 'destinations', 'start', 'end']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class TripsUpdate(LoginRequiredMixin, UpdateView):
  model = Trip
  fields = ['name', 'destinations', 'start', 'end', 'accommodation', 'journal']

class TripsDelete(LoginRequiredMixin, DeleteView):
  model = Trip
  success_url = '/trips/'

class ActivitiesUpdate(LoginRequiredMixin, UpdateView):
  model = Activity 
  fields = ['d_time', 'activity']

class ActivitiesDelete(LoginRequiredMixin, DeleteView):
  model = Activity
  success_url = '/trips/'
  

  
def destinations_create(request):
  pass