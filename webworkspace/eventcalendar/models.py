from django.db import models
from django.contrib.auth.models import User

class Venue(models.Model):
    '''
    Model to represent a venue where events are held. 
    It includes fields for the name, address, zip code, contact phone, website, and email address of the venue.
    '''

    name = models.CharField('Venue Name', max_length=100)
    address = models.CharField('Address', max_length=100)
    zip_code = models.CharField('Zip Code', max_length=10)
    phone = models.CharField('Contact Phone', max_length=15, blank=True)
    website = models.URLField('Website', blank=True)
    email_address = models.EmailField('Email Address', blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    '''
    Model to represent an event in the system.
    It includes fields for the event name, date, venue, and description.
    '''

    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True, related_name='events') # ForeignKey to User model to link events to their respective users
    name = models.CharField('Event Name', max_length=100)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank = True, null = True, on_delete = models.CASCADE, related_name = 'events') # ForeignKey to Venue model to link events to their respective venues
    description = models.TextField('Description', blank=True)

    def __str__(self):
        return self.name