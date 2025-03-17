from django.contrib import admin
from .models import Event # Import the Event model from models.py of same directory

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    '''
    Admin class to customize the admin interface for the Event model.
    It includes a list display and search fields for the event name and date.
    '''

    fields = ('name', 'start_time', 'end_time', 'location', 'description',) # Fields to display in the admin interface
    list_display = ('name', 'start_time', 'location')
    list_filter = ('start_time', 'location',)
    ordering = ('start_time',) # Order the list by event date
    search_fields = ('name',)