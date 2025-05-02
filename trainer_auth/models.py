from django.db import models
from authentication.models import User  

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    bio = models.TextField(blank=True, default="")
    experience = models.TextField(blank=True, default="")
    isAvailableForReservation = models.BooleanField(default=True)
    price = models.FloatField(default=0.0)
    specialties = models.TextField(blank=True, default="")
    certificates = models.TextField(blank=True, default="")

    def __str__(self):
        return self.user.email

    @property
    def rating(self):
        from django.db.models import Avg
        return self.ratings_received.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0.0

class Rating(models.Model):
    trainee = models.ForeignKey('client_auth.Trainee', on_delete=models.CASCADE, related_name='ratings_given')
    trainer = models.ForeignKey('trainer_auth.Trainer', on_delete=models.CASCADE, related_name='ratings_received')
    rating = models.PositiveSmallIntegerField()  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trainee', 'trainer')  
    def __str__(self):
        return f"{self.trainee.user.email} → {self.trainer.user.email} = {self.rating}"
