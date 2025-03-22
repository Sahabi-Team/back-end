from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    TRAINER = 'trainer'
    TRAINEE = 'trainee'
    
    USER_TYPES = [
        (TRAINER, 'Trainer'),
        (TRAINEE, 'Trainee'),
    ]

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    REQUIRED_FIELDS = ['email', 'phone_number', 'user_type']

    def __str__(self):
        return f"{self.username} ({self.user_type})"

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    expertise = models.CharField(max_length=100)
    certifications = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)

    def __str__(self):
        return f"Trainer: {self.user.username}"

class Trainee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainee_profile')
    age = models.IntegerField()
    enrolled_courses = models.TextField(blank=True)

    def __str__(self):
        return f"Trainee: {self.user.username}"
