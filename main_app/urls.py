from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('trips/', views.trips_index, name='index'),
    path('trips/create/', views.TripsCreate.as_view(), name='trips_create'),
]