from django.shortcuts import render
from django.contrib.auth.views import reverse_lazy 

import calendar
from calendar import HTMLCalendar

from datetime import datetime
import zoneinfo

from .models import Event

from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'eventcalendar/login.html' # Custom login template
    redirect_authenticated_user = True # Redirect to home if user is authenticated
    field = '__all__' # All fields are required for login

    def get_success_url(self):
        return reverse_lazy('home') # Redirect to home page after successful login


def home(request, year: int=datetime.now().year, month: str=datetime.now().strftime('%B')):
    '''
    Function to render the home page with a calendar for the specified year and month.
    '''

    name = 'Henny'
    month = month.capitalize() # Capitalizes only the first letter of the month.

    # Convert month from name to number (int)
    month_int = int(list(calendar.month_name).index(month))

    # Create the calendar
    event_calendar = HTMLCalendar().formatmonth(year, month_int)

    # Get current year
    timezone = zoneinfo.ZoneInfo('America/Chicago') # Central Time, may change later
    now = datetime.now(tz=timezone)
    current_year = now.year
    
    # Get current time
    time = now.strftime('%H:%M')

    return render(request, 'eventcalendar/home.html', { # Context dictionary
        'name': name,
        'year': year,
        'month': month,
        'month_int': month_int,
        'event_calendar': event_calendar,
        'current_year': current_year,
        'time': time,
    })


def all_events(request):
    '''
    Function to render the page with all events.
    '''

    event_list = Event.objects.all() # Get all events from the database

    return render(request, 'eventcalendar/event_list.html', 
    {'event_list': event_list
    })
