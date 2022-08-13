from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('trips/', views.trips_index, name='index'),
    path('trips/<int:trip_id>/', views.trips_detail, name='detail'),
    path('trips/create/', views.TripsCreate.as_view(), name='trips_create'),
    path('trips/<int:pk>/update/', views.TripsUpdate.as_view(), name='trips_update'),
    path('trips/<int:pk>/delete/', views.TripsDelete.as_view(), name='trips_delete'),
]