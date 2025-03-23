from django.contrib.auth.models import AbstractUser
from django.db import models
from authentication.models import User
class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    expertise = models.CharField(max_length=100,default="body-building")
    experience_years = models.IntegerField(default=0)

    def __str__(self):
        return self.email
