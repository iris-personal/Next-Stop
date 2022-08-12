from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Trip



# Create your views here.
def home(request):
  return render(request, 'home.html')

def trips_index(request):
  trips = Trip.objects.filter(user=request.user)
  return render(request, 'trips/index.html', {'trips' : trips})

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