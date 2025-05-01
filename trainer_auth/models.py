from django.db import models
from authentication.models import User

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    expertise = models.CharField(max_length=100, default="body-building")
    experience_years = models.IntegerField(default=0)

    def __str__(self):
        return self.user.email

    @property
    def rating(self):
        from django.db.models import Avg
        return self.comments_received.aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or 0.0


class Comment(models.Model):
    trainee = models.ForeignKey('client_auth.Trainee', on_delete=models.CASCADE, related_name='comments_given')
    trainer = models.ForeignKey('trainer_auth.Trainer', on_delete=models.CASCADE, related_name='comments_received')
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trainee', 'trainer')

    def __str__(self):
        return f"{self.trainee.user.email} → {self.trainer.user.email} = {self.rating}"
