from django.db import models
from authentication.models import User
from trainer_auth.models import Trainer
from client_auth.models import Trainee

class Exercise(models.Model):
    DIFFICULTY_LEVELS = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    muscle_group = models.CharField(max_length=50)  
    equipment = models.CharField(max_length=50, blank=True, null=True)  
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='Beginner')

    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="workout_plans")
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name="workout_plans")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Plan by {self.trainer.user.username} for {self.trainee.user.username}"

class WorkoutExercise(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name="exercises")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="workout_exercises")
    sets = models.IntegerField(default=3)
    reps = models.IntegerField(default=10, blank=True, null=True)  
    duration = models.IntegerField(blank=True, null=True)  

    def __str__(self):
        return f"{self.exercise.name} in {self.workout_plan}"
