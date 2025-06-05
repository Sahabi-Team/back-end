from django.db import models
from django.utils import timezone
from authentication.models import User
from mentorship.models import Mentorship

class Message(models.Model):
    mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default=False)
    seen_at = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.content[:30]}"
