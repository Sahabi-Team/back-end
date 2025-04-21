from rest_framework import serializers
from .models import Mentorship
from client_auth.serializers import TraineeSerializer
from trainer_auth.serializers import TrainerSerializer
from trainer_auth.models import Trainer

class MentorshipSerializer(serializers.ModelSerializer):
    trainee = TraineeSerializer(read_only=True)
    trainer = TrainerSerializer(read_only=True)
    trainer_id = serializers.PrimaryKeyRelatedField(
        queryset=Trainer.objects.all(),
        source='trainer',
        write_only=True
    )
    days_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = Mentorship
        fields = ['id', 'trainee', 'trainer', 'trainer_id', 'created_at', 'expires_at', 'is_active', 'days_remaining']
        read_only_fields = ['created_at', 'expires_at']
    
    def get_days_remaining(self, obj):
        """Calculate the number of days remaining until expiration"""
        from django.utils import timezone
        if obj.is_expired():
            return 0
        delta = obj.expires_at - timezone.now()
        return delta.days

class MentorshipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentorship
        fields = ['trainer'] 