from django.db import models
from authentication.models import User  # Import the User model

class Trainee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="trainee_profile")
    height = models.FloatField(blank=True, null=True)  # In cm
    weight = models.FloatField(blank=True, null=True)  # In kg

    def __str__(self):
        return f"Trainee: {self.user.username}"
