from rest_framework import serializers
from .models import Test

class TestSerializer(serializers.ModelSerializer):
    trainee_username = serializers.CharField(source='trainee.user.username', read_only=True)  # Show username instead of ID

    class Meta:
        model = Test
        # fields = '__all__'
        fields = [
            'id', 'trainee', 'trainee_username', 'birth_date', 'gender', 'body_form',
            'weight', 'height', 'goal_weight', 'goal', 'equipment', 'workout_days', 
            'diseases', 'focus_area', 'fitness_level', 'created_at'
        ]
        read_only_fields = ['trainee', 'created_at']  # Ensure trainee is assigned automatically
