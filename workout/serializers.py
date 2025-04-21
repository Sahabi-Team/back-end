from rest_framework import serializers
from .models import WorkoutPlan, WorkoutExercise
from exercise.serializers import ExerciseSerializer 

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer()

    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'sets', 'reps', 'duration']

class WorkoutPlanSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = ['id', 'trainer', 'created_at', 'is_active', 'exercises']
