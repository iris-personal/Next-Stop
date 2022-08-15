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
    path('trips/<int:trip_id>/add_activity/', views.add_activity, name='add_activity'),
    path('trips/<int:pk>/update_activity/', views.ActivitiesUpdate.as_view(), name='activities_update'),
    path('trips/<int:pk>/delete_activity/', views.ActivitiesDelete.as_view(), name='activities_delete'),
    path('destinations/', views.destinations, name='destinations'),
    path('destinations/create/', views.destinations_create, name='destinations_create'),
    path('destinations/search/', views.destinations_search, name='destinations_search'),
]