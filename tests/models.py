from django.db import models
from client_auth.models import Trainee

class Test(models.Model):
    """Model to store fitness test details for a Trainee"""
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name="tests")
    weight = models.FloatField(help_text="Current weight in kg")
    height = models.FloatField(help_text="Height in cm")
    goal_weight = models.FloatField(help_text="Target weight in kg", null=True, blank=True)
    
    GOAL_CHOICES = [
        ('lose_weight', 'Lose Weight'),
        ('gain_muscle', 'Gain Muscle'),
        ('stay_fit', 'Stay Fit'),
    ]
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, help_text="Overall fitness goal")

    WORKOUT_ROOM_CHOICES = [
        ('gym', 'Gym'),
        ('home', 'Home'),
        ('outdoor', 'Outdoor'),
    ]
    workout_room = models.CharField(max_length=10, choices=WORKOUT_ROOM_CHOICES, help_text="Where you prefer to work out")

    workout_time = models.CharField(max_length=50, help_text="Preferred workout time (e.g., Morning, Evening, etc.)")
    illness = models.TextField(blank=True, null=True, help_text="Any illnesses or medical conditions")
    
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    workout_experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, help_text="Workout experience level")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test for {self.trainee.user.username} - {self.goal}"
