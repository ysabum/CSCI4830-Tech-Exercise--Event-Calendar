from django.urls import path
from . import views #Imports the views from the same directory 

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('', views.CalendarView.as_view(), name='calendar'),
    path('new/', views.EventCreateView.as_view(), name='event_new'),
    path('logout/', views.logout_user, name='logout'),
]