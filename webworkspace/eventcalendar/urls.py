from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views #Imports the views from the same directory 

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name = 'login'),
    path('register/', views.RegisterView.as_view(), name = 'register'),
    path('', views.CalendarView.as_view(), name = 'calendar'),
    path('new/', views.EventCreateView.as_view(), name = 'event_new'),
    path('all/', views.EventListView.as_view(), name = 'event_list'),
    path('edit/<int:pk>/', views.EventUpdateView.as_view(), name = 'event_edit'),
    path('delete/<int:pk>/', views.EventDeleteView.as_view(), name = 'event_delete'),
    path('logout/', views.logout_user, name = 'logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)