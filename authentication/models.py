from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Choices for usertype field
    TRAINEE = 'trainee'
    TRAINER = 'trainer'
    USER_TYPE_CHOICES = [
        (TRAINEE, 'Trainee'),
        (TRAINER, 'Trainer'),
    ]

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    usertype = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=TRAINEE)  # Default to 'trainee'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    def get_profile(self):
        """Return the related profile (Trainee or Trainer)"""
        if self.usertype == self.TRAINEE:
            return self.trainee_profile  # Access the related Trainee profile
        elif self.usertype == self.TRAINER:
            return self.trainer_profile  # Access the related Trainer profile
        return None
