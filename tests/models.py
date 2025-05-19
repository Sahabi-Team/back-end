from django.db import models
from client_auth.models import Trainee
from django.core.validators import MinValueValidator, MaxValueValidator

class Test(models.Model):
    """Model to store fitness test details for a Trainee"""
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name="tests")
    birth_date = models.DateField(help_text="Trainee's date of birth")
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, help_text="Trainee's gender")
    body_form = models.FloatField(help_text="Body form score (non-negative number)", validators=[MinValueValidator(0)])
    
    weight = models.FloatField(help_text="Current weight in kg")
    height = models.FloatField(help_text="Height in cm")
    goal_weight = models.FloatField(help_text="Target weight in kg", null=True, blank=True)
    
    GOAL_CHOICES = [
        ('lose_weight', 'Lose Weight'),
        ('gain_muscle', 'Gain Muscle'),
        ('stay_fit', 'Stay Fit'),
    ]
    goal = models.CharField(max_length=20, help_text="Overall fitness goal")

    WORKOUT_ROOM_CHOICES = [
        ('باشگاه', 'Gym'),
        ('خونه', 'Home'),
        ('بیرون', 'Outdoor'),
    ]
    equipment = models.CharField(max_length=20, help_text="Where you prefer to work out")

    workout_days = models.CharField(max_length=50, help_text="Preferred workout time (e.g., Morning, Evening, etc.)")
    diseases = models.TextField(blank=True, null=True, help_text="Any illnesses or medical conditions")
    
    FOCUS_AREA_CHOICES = [
        ('arms', 'Arms'),
        ('legs', 'Legs'),
        ('core', 'Core'),
        ('back', 'Back'),
        ('chest', 'Chest'),
        ('full_body', 'Full Body'),
    ]
    focus_area = models.CharField(max_length=20, help_text="Primary body area to focus on")
    
    fitness_level = models.IntegerField(
        help_text="Workout experience level (1-6)",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(6)
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test for {self.trainee.user.username} - {self.goal}"
