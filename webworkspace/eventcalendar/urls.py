from django.urls import path
from . import views #Imports the views from the same directory 

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<str:month>/', views.home, name='home'),
]