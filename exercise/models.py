from django.db import models

class ExerciseTag(models.Model):
    """Predefined tags for exercises (e.g., 'aerobics', 'strength')"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    """Exercise model containing images, description, and tags"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField(ExerciseTag, related_name="exercises")

    def __str__(self):
        return self.name

class ExerciseImage(models.Model):
    """Images related to an exercise"""
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="exercise_images/")  # Store in media/exercise_images

    def __str__(self):
        return f"Image for {self.exercise.name}"
