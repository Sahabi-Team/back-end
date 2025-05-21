from django.db import models
from authentication.models import User

class Ticket(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    email = models.EmailField(null=True)
    name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.name}"
