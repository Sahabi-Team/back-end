from django.contrib.auth.models import AbstractUser
from django.db import models

class Client(AbstractUser):
    email = models.EmailField(unique=True) 
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    trainers = models.ManyToManyField(
        'trainer_auth.Trainer', related_name='clients', blank=True,
        help_text="Trainers that this client has selected for workouts."
    )

    groups = models.ManyToManyField(
        'auth.Group', related_name='client_set', blank=True, 
        help_text='The groups this user belongs to.'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='client_permissions', blank=True, 
        help_text='Specific permissions for this user.'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        return self.email 
