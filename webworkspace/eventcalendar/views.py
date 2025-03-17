from django.shortcuts import render, redirect
from django.contrib.auth.views import reverse_lazy 
from django.http import HttpResponse

from datetime import datetime, timedelta, date
import calendar

from .models import Event
from .forms import EventForm
from .utils import Calendar

from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe


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

        return reverse_lazy('calendar') # Redirect to home page after successful login


def logout_user(request):
    '''
    Function to handle user logout.
    '''

    logout(request) # Logout the user
    return redirect('login') # Redirect to login page after logout


class CalendarView(LoginRequiredMixin, ListView):
    '''
    Class-based view to render the home page. Home page contains the calendar for today's date.
    Requires user to be authenticated.
    '''

    model = Event
    template_name = 'eventcalendar/calendar.html'

    def get_date(self, req_day):
        if req_day:
            year, month = (int(x) for x in req_day.split('-'))
            return date(year, month, day = 1)

        return datetime.today()

    def previous_month(self, cal_day):
        first = cal_day.replace(day = 1)
        previous_month = first - timedelta(days = 1)
        month = 'month=' + str(previous_month.year) + '-' + str(previous_month.month)

        return month

    def next_month(self, cal_day):
        days_in_month = calendar.monthrange(cal_day.year, cal_day.month)[1]
        last = cal_day.replace(day = days_in_month)
        next_month = last + timedelta(days = 1)
        month = 'month=' + str(next_month.year) + '-' + str(next_month.month)

        return month

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cal_day = self.get_date(self.request.GET.get('month', None))

        event_calendar = Calendar(cal_day.year, cal_day.month)
        html_calendar = event_calendar.formatmonth(withyear = True)

        context['calendar'] = mark_safe(html_calendar)
        context['prev_month'] = self.previous_month(cal_day)
        context['next_month'] = self.next_month(cal_day)

        return context


class EventCreateView(LoginRequiredMixin, CreateView):
    '''
    Class-based view to create a new event.
    Requires user to be authenticated.
    '''

    def get(self, request, event_id = None):
        instance = Event()
        if event_id:
            instance = get_object_or_404(Event, pk = event_id)
        else:
            instance = Event()

        form = EventForm(request.POST or None, instance=instance)

        if request.POST and form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('eventcalendar:calendar'))

        return render(request, 'eventcalendar/event.html', {'form': form})