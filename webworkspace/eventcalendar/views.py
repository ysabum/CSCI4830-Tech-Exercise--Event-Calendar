from django.shortcuts import render, redirect
from django.contrib.auth.views import reverse_lazy 
from django.http import HttpResponse, HttpResponseRedirect

from datetime import datetime, timedelta, date
import calendar

from .models import Event
from .forms import EventForm
from .utils import Calendar

from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
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


class RegisterView(FormView):
    '''
    Class-based view to handle user registration.
    '''

    template_name = 'eventcalendar/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('calendar')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)

        return redirect('login')


def logout_user(request):
    '''
    Function to handle user logout.
    '''

    logout(request) # Logout the user
    return redirect('login') # Redirect to login page after logout


class CalendarView(LoginRequiredMixin, ListView):
    '''
    Class-based view to render the home page.
    Ensures users only see their own events.
    Requires user to be authenticated.
    '''

    model = Event
    template_name = 'eventcalendar/calendar.html'


    def get_date(self, req_day): # req_day = requested year and month
        '''
        Function to get the date.
        '''

        if req_day:
            try:
                year, month = (int(x) for x in req_day.split('-'))
                return date(year, month, 1)

            except ValueError:
                pass  # In case of an invalid format, fallback to today
    
        return datetime.today().date()


    def previous_month(self, cal_day):
        '''
        Function to get the previous month.
        '''

        first_day = cal_day.replace(day = 1)
        previous_month = first_day - timedelta(days = 1)

        return f'month={previous_month.year}-{previous_month.month}'


    def next_month(self, cal_day):
        '''
        Function to get the next month.
        '''

        days_in_month = calendar.monthrange(cal_day.year, cal_day.month)[1]
        last_day = cal_day.replace(day = days_in_month)
        next_month = last_day + timedelta(days = 1)

        return f'month={next_month.year}-{next_month.month}'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cal_day = self.get_date(self.request.GET.get('month', None))

        # Fetch only the logged-in user's events
        user_events = Event.objects.filter(
            user = self.request.user,
            start_time__year = cal_day.year,
            start_time__month = cal_day.month
        )

        event_calendar = Calendar(cal_day.year, cal_day.month)
        html_calendar = event_calendar.formatmonth(events = user_events, withyear = True)

        context['calendar'] = mark_safe(html_calendar)
        context['previous_month'] = self.previous_month(cal_day)
        context['next_month'] = self.next_month(cal_day)
        context['events'] = user_events  # Pass filtered events to the template

        return context


class EventListView(LoginRequiredMixin, ListView):
    '''
    Class-based view to list all events for the logged-in user.
    '''

    model = Event
    template_name = 'eventcalendar/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        '''
        Function to get the queryset.
        Returns only the events for the logged-in user, optionally filtered by search query.
        '''

        query = self.request.GET.get('q', '')  # Get search query from URL
        queryset = Event.objects.filter(user = self.request.user)

        if query:
            queryset = queryset.filter(name__icontains = query)  # Case-insensitive search

        return queryset

    def get_context_data(self, **kwargs):
        '''
        Function to pass additional context to the template.
        Includes the search query in the context for display in the template.
        '''
        
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Pass query to the template

        return context


class EventCreateView(LoginRequiredMixin, CreateView):
    '''
    Class-based view to create a new event.
    '''

    model = Event
    form_class = EventForm
    template_name = 'eventcalendar/event.html'
    success_url = reverse_lazy('calendar')


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventCreateView, self).form_valid(form)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    '''
    Class-based view to update an existing event.
    '''

    model = Event
    form_class = EventForm
    template_name = 'eventcalendar/event_edit.html'
    success_url = reverse_lazy('calendar')


class EventDeleteView(LoginRequiredMixin, DeleteView):
    '''
    Class-based view to delete an event.
    Ensures only the event owner can delete it.
    '''
    model = Event
    template_name = 'eventcalendar/delete.html'  # Confirmation template
    success_url = reverse_lazy('calendar')

    def get_queryset(self):
        return Event.objects.filter(user = self.request.user)

    # Handle the confirmation page
    def get(self, request, *args, **kwargs):
        context = {
            'event': self.get_object()
        }

        return self.render_to_response(context)

    # Handle the deletion when the user confirms
    def post(self, request, *args, **kwargs):
        event = self.get_object()
        event.delete()

        return HttpResponseRedirect(self.success_url)
