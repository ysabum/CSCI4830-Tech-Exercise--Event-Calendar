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
    

class Calendar_User(models.Model):
    '''
    Model to represent a user in the system. 
    It includes fields for the user's name, email, and password.
    '''

    first_name = models.CharField('First Name', max_length=100)
    last_name = models.CharField('Last Name', max_length=100)
    email = models.EmailField('Email Address', unique=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    '''
    Model to represent an event in the system.
    It includes fields for the event name, date, venue, and description.
    '''

    name = models.CharField('Event Name', max_length=100)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank = True, null = True, on_delete=models.CASCADE, related_name='events') # ForeignKey to Venue model to link events to their respective venues
    description = models.TextField('Description', blank=True)
    attendees = models.ManyToManyField(Calendar_User, blank=True) # ManyToManyField to Users model to link users to events they are attending

    def __str__(self):
        return self.name