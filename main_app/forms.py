from django.forms import ModelForm
from .models import Activity
from django import forms


# class DateInput(forms.DateInput):
#     input_type = 'datetime-local'

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['a_date','a_time', 'activity']
        # widgets = {
        #     'a_time': DateInput(),
        # }

