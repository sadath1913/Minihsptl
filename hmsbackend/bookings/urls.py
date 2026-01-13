from django.urls import path
from . import views

urlpatterns = [
    path('slots/', views.available_slots, name='available_slots'),
    path('book/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    # 👇 NEW (doctor)
    path('doctor/bookings/', views.doctor_booked_appointments, name='doctor_bookings'),
    path('doctor/bookings/cancel/<int:booking_id>/',views.cancel_appointment,name='cancel_appointment'),

]
