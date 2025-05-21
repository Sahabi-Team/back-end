from rest_framework import serializers
from .models import Test
from mentorship.models import Mentorship

class TestSerializer(serializers.ModelSerializer):
    trainee_username = serializers.CharField(source='trainee.user.username', read_only=True)  # Show username instead of ID
    trainee_name = serializers.CharField(source='trainee.user.name', read_only=True)
    mentorship_id = serializers.SerializerMethodField()

    class Meta:
        model = Test
        # fields = '__all__'
        fields = [
            'id', 'trainee', 'trainee_username', 'trainee_name', 'birth_date', 'gender', 'body_form',
            'weight', 'height', 'goal_weight', 'goal', 'equipment', 'workout_days', 
            'diseases', 'focus_area', 'fitness_level', 'created_at', 'mentorship_id'
        ]
        read_only_fields = ['trainee', 'created_at']  # Ensure trainee is assigned automatically

    def get_mentorship_id(self, obj):
        # Get the active mentorship between the trainee and the requesting trainer
        request = self.context.get('request')
        if request and hasattr(request.user, 'trainer_profile'):
            mentorship = Mentorship.objects.filter(
                trainee=obj.trainee,
                trainer=request.user.trainer_profile,
                is_active=True
            ).first()
            return mentorship.id if mentorship else None
        return None
