from django.contrib import admin
from .models import Trip, Activity, Destination

# Register your models here.

admin.site.register(Trip)
admin.site.register(Activity)
admin.site.register(Destination)