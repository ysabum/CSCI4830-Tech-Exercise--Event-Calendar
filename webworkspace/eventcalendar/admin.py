from django.contrib import admin
from .models import Event, Venue, Calendar_User # Import the Event model from models.py of same directory

#admin.site.register(Venue) # Register the Venue model with the admin site
admin.site.register(Calendar_User) # Register the Users model with the admin site
#admin.site.register(Event) # Register the Event model with the admin site

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    '''
    Admin class to customize the admin interface for the Venue model.
    It includes a list display and search fields for the venue name and address.
    '''

    list_display = ('name', 'address', 'zip_code', 'email_address')
    ordering = ('name',) # Order the list by name
    search_fields = ('name', 'address')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    '''
    Admin class to customize the admin interface for the Event model.
    It includes a list display and search fields for the event name and date.
    '''

    fields = (('name', 'venue',), 'event_date', 'description', 'attendees',) # Fields to display in the admin form
    list_display = ('name', 'event_date', 'venue',)
    list_filter = ('event_date', 'venue',)
    ordering = ('event_date',) # Order the list by event date
    search_fields = ('name', 'event_date',)