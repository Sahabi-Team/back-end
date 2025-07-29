from rest_framework import serializers
from .models import WorkoutPlan, WorkoutExercise
from exercise.serializers import ExerciseSerializer

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise_id = serializers.IntegerField(write_only=True)
    workout_plan_id = serializers.IntegerField(write_only=True, required=False)
    exercise_name = serializers.SerializerMethodField()
    exercise_id_display=serializers.SerializerMethodField()
    class Meta:
        model = WorkoutExercise
        fields = [
            'id', 'exercise_id', 'exercise_name', 'workout_plan_id', 'sets', 'reps',
            'duration', 'description', 'order', 'day','exercise_id_display'
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'sets': {'help_text': 'Number of sets for this exercise'},
            'reps': {'help_text': 'Number of repetitions per set (optional if duration is provided)'},
            'duration': {'help_text': 'Duration in seconds (optional if reps is provided)'},
            'description': {'help_text': 'Additional instructions or notes for this exercise'},
            'order': {'help_text': 'Order of the exercise in the workout plan'},
            'day': {'help_text': 'Day number this exercise is scheduled for'}
        }

    def validate(self, data):
        if not data.get('reps') and not data.get('duration'):
            raise serializers.ValidationError("Either reps or duration must be provided.")
        if data.get('reps') and data.get('duration'):
            raise serializers.ValidationError("Provide either reps or duration, not both.")
        return data

    def get_exercise_name(self, obj):
        return obj.exercise.name
    def get_exercise_id_display(self, obj):
        return obj.exercise.id



class WorkoutPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for workout plans.
    
    This serializer handles the creation and retrieval of workout plans.
    It includes the plan details and associated exercises.
    """
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)
    trainer_name = serializers.SerializerMethodField(
        help_text="Username of the trainer who created the workout plan"
    )
    trainer_namee = serializers.SerializerMethodField(
        help_text="Name of the trainer who created the workout plan"
    )

    class Meta:
        model = WorkoutPlan
        fields = ['id', 'mentorship', 'status', 'name', 'description', 'created_at', 'updated_at', 'exercises', 'trainer_name', 'trainer_namee']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'mentorship': {'help_text': 'ID of the mentorship this workout plan belongs to'},
            'name': {'help_text': 'Name of the workout plan'},
            'description': {'help_text': 'Detailed description of the workout plan'}
        }

    def get_trainer_name(self, obj):
        return obj.mentorship.trainer.user.username
    
    def get_trainer_namee(self, obj):
        return obj.mentorship.trainer.user.name
