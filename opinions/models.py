from django.db import models
from authentication.models import User

class Opinion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="opinion")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Opinion by {self.user.username}"
