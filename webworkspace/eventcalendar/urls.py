from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views # Imports the views from the same directory 

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name = 'login'), # Login
    path('register/', views.RegisterView.as_view(), name = 'register'), # Register
    path('', views.CalendarView.as_view(), name = 'calendar'), # Main Calendar/Home
    path('new/', views.EventCreateView.as_view(), name = 'event_new'), # Add Event
    path('all/', views.EventListView.as_view(), name = 'event_list'), # Event List
    path('edit/<int:pk>/', views.EventUpdateView.as_view(), name = 'event_edit'), # Edit Event
    path('delete/<int:pk>/', views.EventDeleteView.as_view(), name = 'event_delete'), # Delete Event
    path('logout/', views.logout_user, name = 'logout'), # Logout
]

# Defunct? Was originally added so users could upload a picture of the event, but that functionality was removed...
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)