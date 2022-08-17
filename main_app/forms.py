from django.forms import ModelForm
from .models import Activity
from django import forms


class DateInput(forms.DateInput):
    input_type = 'datetime-local'

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['d_time', 'activity']
        widgets = {
            'd_time': DateInput(),
        }

