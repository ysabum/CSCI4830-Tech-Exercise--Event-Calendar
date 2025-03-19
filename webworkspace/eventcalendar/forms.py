from django import forms
from django.forms import ModelForm
from .models import Event

class EventForm(ModelForm):
    '''
    Form to create and update events.
    '''
    
    class Meta:
        model = Event
        fields = ['name', 'start_time', 'end_time', 'location', 'description',]