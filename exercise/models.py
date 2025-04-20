from django.db import models

class ExerciseTag(models.Model):
    """Predefined tags for exercises (e.g., 'aerobics', 'strength')"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class MuscleGroup(models.Model):
    """Predefined muscle groups for exercises"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    """Predefined equipment for exercises"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    """Exercise model containing images, description, and tags"""
    DIFFICULTY_LEVELS = [
        ('مبتدی', 'مبتدی'),
        ('متوسط', 'متوسط'),
        ('پیشرفته', 'پیشرفته'),
    ]
    WORKOUT_PLACES = [
        ('باشگاه', 'باشگاه'),
        ('خانه', 'خانه'),
    ]
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField(ExerciseTag, related_name="exercises")
    muscle_groups = models.ManyToManyField(MuscleGroup, related_name="exercises")
    equipments = models.ManyToManyField(Equipment, related_name="exercises", blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='مبتدی')
    workoutplaces = models.CharField(max_length=20, choices=WORKOUT_PLACES, default='خانه')

    def __str__(self):
        return self.name

class ExerciseImage(models.Model):
    """Images related to an exercise"""
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="exercise_images/")  # Store in media/exercise_images

    def __str__(self):
        return f"Image for {self.exercise.name}"
