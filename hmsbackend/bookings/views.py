from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db import transaction
from datetime import datetime
from django.shortcuts import get_object_or_404
from scheduling.models import Availability
from .models import Booking
from .utils import create_calendar_event
from .email_service import send_email_notification

@login_required
def available_slots(request):
    if request.user.role != 'patient':
        return HttpResponseForbidden("Access denied")

    slots = Availability.objects.filter(is_booked=False)
    return render(request, 'bookings/available_slots.html', {'slots': slots})


@login_required
@transaction.atomic
def book_slot(request, slot_id):
    if request.user.role != 'patient':
        return HttpResponseForbidden("Access denied")

    slot = Availability.objects.select_for_update().get(id=slot_id)

    if slot.is_booked:
        return render(request, 'bookings/already_booked.html')

    # Create booking
    Booking.objects.create(
        doctor=slot.doctor,
        patient=request.user,
        availability=slot
    )

    # Mark slot as booked
    slot.is_booked = True
    slot.save()
    # Send email notifications
    # Send booking confirmation email to patient
    send_email_notification(
        email_type="BOOKING_CONFIRMATION",
        to_email=request.user.email,
        username=request.user.username
    )

    #  Send booking email to doctor
    send_email_notification(
        email_type="BOOKING_CONFIRMATION",
        to_email=slot.doctor.email,
        username=slot.doctor.username
    )

    # Calendar times
    start = datetime.combine(slot.date, slot.start_time)
    end = datetime.combine(slot.date, slot.end_time)

    # Patient calendar
    create_calendar_event(
        request.user,
        f"Appointment with Dr. {slot.doctor.username}",
        start.isoformat(),
        end.isoformat()
    )

    # Doctor calendar
    create_calendar_event(
        slot.doctor,
        f"Appointment with {request.user.username}",
        start.isoformat(),
        end.isoformat()
    )

    return redirect('patient_dashboard')

@login_required
def my_appointments(request):
    if request.user.role != 'patient':
        return HttpResponseForbidden("Access denied")

    appointments = Booking.objects.filter(patient=request.user).select_related(
        'doctor', 'availability'
    ).order_by('-availability__date')

    return render(
        request,
        'bookings/my_appointments.html',
        {'appointments': appointments}
    )

@login_required
def doctor_booked_appointments(request):
    if request.user.role != 'doctor':
        return HttpResponseForbidden("Access denied")

    bookings = Booking.objects.filter(
        doctor=request.user
    ).select_related(
        'patient', 'availability'
    ).order_by('-availability__date', '-availability__start_time')

    return render(
        request,
        'bookings/doctor_booked_appointments.html',
        {'bookings': bookings}
    )

@login_required
@transaction.atomic
def cancel_appointment(request, booking_id):
    if request.user.role != 'doctor':
        return HttpResponseForbidden("Access denied")

    booking = get_object_or_404(Booking, id=booking_id)

    # Ensure doctor owns this appointment
    if booking.doctor != request.user:
        return HttpResponseForbidden("You cannot cancel this appointment")

    slot = booking.availability

    # Delete booking
    booking.delete()

    # Mark slot as free again
    slot.is_booked = False
    slot.save()

    return redirect('doctor_bookings')