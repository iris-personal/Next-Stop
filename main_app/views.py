from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from .models import Trip, Activity
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
      user = form.save()
      login(request, user)
      return redirect('index')
  else: 
    error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def destinations(request):
  return render(request, 'destinations.html')

def destinations_search(request):
  cityId = random.randint(6576468, 10936014)
  secret_key = os.environ['SECRET_KEY']
  access_key = os.environ['ACCESS_KEY']
  encoded_bytes = base64.b64encode(f'{access_key}:{secret_key}'.encode('utf-8'))
  auth_key = str(encoded_bytes, 'utf-8')
  headers = {
    'Authorization': f'Basic {auth_key}'
  }
  response = requests.get(f'https://api.roadgoat.com/api/v2/destinations/{cityId}', headers=headers)
  data = response.json()
  print(cityId)
  budget = data['data']['attributes']['budget']
  if budget == {}:
    text = 'unknown'
  else: 
    budgetText = budget[(list(budget.keys())[0])]
    text = budgetText['subText']
  
  safety = data['data']['attributes']['safety']
  if safety == {}:
    safetyRating = 'unknown'
  else: 
    safetyText = safety[(list(safety.keys())[0])] 
    safetyRating = safetyText['subText']
  
  covid = data['data']['attributes']['covid']
  covidText = covid[(list(covid.keys())[0])]
  covidRating = covidText['text']
  
  avgRating = data['data']['attributes']['average_rating']
  avgRatingCond = '{:.2f}'.format(avgRating)
  
  for item in data['included']:
    if item['type'] == 'photo' and int(item['id']) != 549 and int(item['id']) != 683:
      photos = item['attributes']['image']['medium']
    else:
      photos = 'https://i.imgur.com/XqW2YV0m.jpg'
  
  slugs = []
  for item in data['included']:
    if item['type'] == 'known_for':
      slugs.append(item['attributes']['slug'])

  return render(request, 'destinations.html', {
   'data': data,
   'text': text,
   'safetyRating': safetyRating,
   'covidRating': covidRating,
   'photos': photos,
   'slugs': slugs,
   'avgRatingCond': avgRatingCond
  })

@login_required
def add_activity(request, trip_id):
  form = ActivityForm(request.POST)
  if form.is_valid():
    new_activity = form.save(commit=False)
    new_activity.trip_id = trip_id
    new_activity.save()
  return redirect('detail', trip_id=trip_id)

class TripsCreate(LoginRequiredMixin, CreateView):
  model = Trip
  fields = ['name', 'destinations', 'start', 'end', 'accommodation', 'notes']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class TripsUpdate(LoginRequiredMixin, UpdateView):
  model = Trip
  fields = ['name', 'destinations', 'start', 'end', 'accommodation', 'notes']

class TripsDelete(LoginRequiredMixin, DeleteView):
  model = Trip
  success_url = '/trips/'

class ActivitiesUpdate(LoginRequiredMixin, UpdateView):
  model = Activity 
  fields = ['a_time, a_date', 'activity', 'notes']
  success_url = '/trips/{trip_id}/'

class ActivitiesDelete(LoginRequiredMixin, DeleteView):
  model = Activity
  success_url = '/trips/{trip_id}/'
  
