from django.urls import path
from . import views #Imports the views from the same directory 

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('', views.HomeView.as_view(), name='home'),
    path('<int:year>/<str:month>/', views.HomeView.as_view(), name='home'),
    path('events/', views.EventList.as_view(), name ='all_events'),
    path('logout/', views.logout_user, name='logout'),
]