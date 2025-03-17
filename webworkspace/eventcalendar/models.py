from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse


class Event(models.Model):
    '''
    Model to represent an event in the system.
    It includes fields for the event name, date, venue, and description.
    '''

    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True, related_name='events') # ForeignKey to User model to link events to their respective users
    name = models.CharField('Event Name', max_length=100)
    start_time = models.DateTimeField('Start Time', help_text='Start time of the event.')
    end_time = models.DateTimeField('End Time', help_text='End time of the event.')
    location = models.CharField('Location', help_text='Location of the event.', max_length=100, blank=True)
    description = models.TextField('Description', blank=True)    

    class Meta():
        verbose_name = 'Event Scheduling'
        verbose_name_plural = 'Event Scheduling'

    def __str__(self):
        return self.name