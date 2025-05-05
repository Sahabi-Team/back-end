from django.db import models
from django.utils import timezone
from datetime import timedelta
from client_auth.models import Trainee
from trainer_auth.models import Trainer
from django.apps import apps

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
        is_new = self.pk is None  # Check if this is a new mentorship
        # Set expiration date to 6 months from creation
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=180)  # 6 months
        super().save(*args, **kwargs)
        
        # Create notification for the trainer if this is a new mentorship
        if is_new:
            Notification = apps.get_model('notification', 'Notification')
            Notification.objects.create(
                user=self.trainer.user,
                mentorship=self,
                message=f"سلام معین این صرفا یه مسیجه تستیه میتونی از همونی که خودت نوشتی استفاده کنی"
            )

    def is_expired(self):
        """Check if the mentorship has expired"""
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.trainee.user.username} mentored by {self.trainer.user.username} (Expires: {self.expires_at.strftime('%Y-%m-%d')})"
