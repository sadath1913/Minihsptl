from django.db import models
from accounts.models import User
#This model stores a doctor’s available time slots and tracks whether they are booked.
class Availability(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'doctor'}
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor.username} | {self.date} | {self.start_time}-{self.end_time}"
