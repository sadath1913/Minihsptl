from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .forms import AvailabilityForm
from .models import Availability


@login_required
def add_availability(request):
    if request.user.role != 'doctor':
        return HttpResponseForbidden("Access denied")

    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.doctor = request.user
            availability.save()
            # ✅ redirect to improved My Slots page
            return redirect('my_slots')
    else:
        form = AvailabilityForm()

    return render(request, 'scheduling/add_availability.html', {'form': form})


@login_required
def my_slots(request):
    if request.user.role != 'doctor':
        return HttpResponseForbidden("Access denied")

    slots = Availability.objects.filter(
        doctor=request.user
    ).order_by('-date', '-start_time')

    return render(
        request,
        'scheduling/my_slots.html',
        {'slots': slots}
    )
