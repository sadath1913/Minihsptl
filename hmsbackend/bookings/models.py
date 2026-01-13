from django.db import models
from accounts.models import User
from scheduling.models import Availability

class Booking(models.Model):
    doctor = models.ForeignKey(
        User,
        related_name='doctor_bookings',
        on_delete=models.CASCADE
    )
    patient = models.ForeignKey(
        User,
        related_name='patient_bookings',
        on_delete=models.CASCADE
    )
    availability = models.OneToOneField(
        Availability,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} -> {self.doctor.username}"
