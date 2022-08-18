from django.forms import ModelForm
from .models import Activity
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['a_date','a_time', 'activity', 'notes']
        widgets = {
            'a_date': DateInput(),
            'a_time': TimeInput()
        }

