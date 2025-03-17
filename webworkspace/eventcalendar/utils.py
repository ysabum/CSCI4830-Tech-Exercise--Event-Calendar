from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event

class Calendar(HTMLCalendar):
	'''
	Class to generate a calendar for the specified month and year.
	'''

	def __init__(self, year = None, month = None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# Formats a day as a td (HTML, standard data cell)
	# Filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(start_time__day = day)
		cal_day = ''
		for event in events_per_day:
			cal_day += f'<li> {event.name} </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {cal_day} </ul></td>"

		return '<td></td>'

	# Formats a week as a tr (HTML, defines a row in a table)
	def formatweek(self, the_week, events):
		cal_week = ''
		for cal_day, week_day in the_week:
			cal_week += self.formatday(cal_day, events)

		return f'<tr> {cal_week} </tr>'

	# Formats a month as a table
	# Filter events by year and month
	def formatmonth(self, withyear = True):
		events = Event.objects.filter(start_time__year = self.year, start_time__month = self.month)

		event_calendar = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		event_calendar += f'{self.formatmonthname(self.year, self.month, withyear = withyear)}\n'
		event_calendar += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			event_calendar += f'{self.formatweek(week, events)}\n'

		return event_calendar