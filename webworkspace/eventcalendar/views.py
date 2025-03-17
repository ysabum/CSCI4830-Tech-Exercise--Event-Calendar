from django.shortcuts import render, redirect
from django.contrib.auth.views import reverse_lazy 

import calendar
from calendar import HTMLCalendar

from datetime import datetime
import zoneinfo

from .models import Event

from django.views.generic import TemplateView, ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginView(LoginView):
    '''
    Class-based view to handle user login.
    Uses Django's built-in LoginView.
    '''

    template_name = 'eventcalendar/login.html' 
    redirect_authenticated_user = True # Redirect to home if user is authenticated
    field = '__all__' # All fields are required for login

    def get_success_url(self):
        '''
        Function to redirect user after successful login.
        Returns the URL to redirect to.
        '''

        return reverse_lazy('home') # Redirect to home page after successful login


def logout_user(request):
    '''
    Function to handle user logout.
    '''

    logout(request) # Logout the user
    return redirect('login') # Redirect to login page after logout


class HomeView(LoginRequiredMixin, TemplateView):
    '''
    Class-based view to render the home page.
    Requires user to be authenticated.
    '''

    template_name = 'eventcalendar/home.html' # Template to render the home page

    def get(self, request, year: int=datetime.now().year, month: str=datetime.now().strftime('%B')):
        '''
        Function to handle GET request for the home page.
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


class EventList(LoginRequiredMixin, ListView):
    '''
    Class-based view to render the list of all events.
    Requires user to be authenticated.
    '''

    model = Event 
    template_name = 'eventcalendar/event_list.html' 
    context_object_name = 'event_list' 