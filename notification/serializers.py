from rest_framework import serializers
from .models import Notification
from authentication.models import User
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class TraineeInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id')
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'name', 'profile_picture']

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return f"{settings.PRODUCTION_DOMAIN}{obj.profile_picture.url}"
        else:
            return None

class NotificationSerializer(serializers.ModelSerializer):
    trainee_info = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'user', 'mentorship', 'message', 'is_read', 'created_at', 'read_at', 'trainee_info']
        read_only_fields = ['id', 'created_at', 'read_at']

    def get_trainee_info(self, obj):
        trainee = obj.mentorship.trainee.user
        return TraineeInfoSerializer(trainee).data

    def get_created_at(self, obj):
        now = timezone.now()
        time_diff = now - obj.created_at
        
        if time_diff >= timedelta(days=2):
            # Return exact date for differences >= 2 days
            return obj.created_at.strftime('%Y-%m-%d')
        elif time_diff >= timedelta(days=1):
            # Return "دیروز" for differences between 24-48 hours
            return "دیروز"
        elif time_diff >= timedelta(hours=1):
            # Return hours for differences < 24 hours
            hours = int(time_diff.total_seconds() / 3600)
            return f"{hours} ساعت پیش" 
        else:
            # Return minutes for differences < 1 hour
            minutes = int(time_diff.total_seconds() / 60)
            return f"{minutes} دقیقه پیش" 