from django.db import models
from mentorship.models import Mentorship
from exercise.models import Exercise

class WorkoutPlan(models.Model):
    """
    Model representing a workout plan created by a trainer for a specific mentorship.
    Each workout plan belongs to a mentorship and can have multiple exercises.
    """
    mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE, related_name='workout_plans')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.mentorship}"

class WorkoutExercise(models.Model):
    """
    Model representing an exercise within a workout plan.
    Each workout exercise belongs to a workout plan and references an exercise.
    """
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField(null=True, blank=True)  # Null if duration is used
    duration = models.PositiveIntegerField(null=True, blank=True)  # Duration in seconds, null if reps is used
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)  # To maintain exercise order in the workout

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.exercise.name} in {self.workout_plan.name}"
