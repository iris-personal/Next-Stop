from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from .models import Trip



# Create your views here.
def home(request):
  return render(request, 'home.html')

def trips_index(request):
  trips = Trip.objects.filter(user=request.user)
  return render(request, 'trips/index.html', {'trips' : trips})

def trips_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    return render(request, 'trips/detail.html', {'trip': trip})

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

class TripsCreate(LoginRequiredMixin, CreateView):
    model = Trip
    fields = ['name', 'destinations', 'start', 'end']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
