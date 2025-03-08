from django.contrib.auth.models import AbstractUser
from django.db import models

class Trainer(AbstractUser):
    
    # ROLE_CHOICES = [('trainer', 'Trainer')]
    
    phone_number = models.CharField(max_length=15, unique=True)
    # role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='trainer')

    groups = models.ManyToManyField(
        'auth.Group', related_name='trainer_set', blank=True, help_text='The groups this user belongs to.'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='trainer_permissions', blank=True, help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.username
