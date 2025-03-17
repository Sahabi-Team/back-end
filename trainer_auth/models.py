from django.contrib.auth.models import AbstractUser
from django.db import models

class Trainer(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)



    groups = models.ManyToManyField(
        'auth.Group', related_name='trainer_set', blank=True,
        help_text='The groups this user belongs to.'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='trainer_permissions', blank=True,
        help_text='Specific permissions for this user.'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
