from django.contrib.auth.models import AbstractUser
from django.db import models
#We extend Django’s AbstractUser to add a role field for Doctor and Patient.
class User(AbstractUser):
    role = models.CharField(max_length=10)
    google_token = models.JSONField(null=True, blank=True)