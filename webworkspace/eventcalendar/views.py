from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
import zoneinfo

def home(request, year: int=datetime.now().year, month: str=datetime.now().strftime('%B')):
    '''
    Function to render the home page with a calendar for the specified year and month.

    Parameters:
    request (HttpRequest): The HTTP request object.
    year (int): The year for which the calendar is to be displayed.
    month (str): The name of the month for which the calendar is to be displayed.

    Output:
    Renders the 'home.html' template with the calendar and other context variables.
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
