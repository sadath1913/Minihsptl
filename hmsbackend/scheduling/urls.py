from django.urls import path
from . import views

urlpatterns = [
    path('doctor/availability/add/', views.add_availability, name='add_availability'),
    path('doctor/availability/', views.my_slots, name='my_slots'),
]
