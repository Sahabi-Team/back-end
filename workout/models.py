from django.db import models
from mentorship.models import Mentorship
from exercise.models import Exercise

class WorkoutPlan(models.Model):
    """
    Model representing a workout plan created by a trainer for a specific mentorship.
    Each workout plan belongs to a mentorship and can have multiple exercises.
    """
    mentorship = models.ForeignKey(
        Mentorship, 
        on_delete=models.CASCADE, 
        related_name='workout_plans',
        null=True,  # Allow null temporarily for migration
        blank=True  # Allow blank temporarily for migration
    )
    STATUS_CHOICES = [
        ('تمام شده', 'تمام شده'),
        ('شروع نشده', 'شروع نشده'),
        ('در حال انجام', 'در حال انجام'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, default='در حال انجام', choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.mentorship}"

class WorkoutExercise(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    day = models.PositiveIntegerField(help_text="Day number of the workout plan this exercise is scheduled for", default=1)  # ✅ New field

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.exercise.name} in {self.workout_plan.name}"
