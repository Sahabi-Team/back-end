from django.db import models
from django.utils import timezone
from datetime import timedelta
from client_auth.models import Trainee
from trainer_auth.models import Trainer

class Mentorship(models.Model):
    """
    Model representing a mentorship connection between a trainer and a trainee.
    The connection expires after 6 months from the creation date.
    """
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='mentorships')
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='mentorships')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(editable=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Set expiration date to 6 months from creation
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=180)  # 6 months
        super().save(*args, **kwargs)

    def is_expired(self):
        """Check if the mentorship has expired"""
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.trainee.user.username} mentored by {self.trainer.user.username} (Expires: {self.expires_at.strftime('%Y-%m-%d')})"
