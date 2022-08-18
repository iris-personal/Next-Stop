from django.forms import ModelForm
from .models import Activity
from django import forms


class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['a_date','a_time', 'activity', 'notes']

