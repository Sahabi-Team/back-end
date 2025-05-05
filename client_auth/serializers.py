from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Trainee
from authentication.models import User

class TraineeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    trainee_id = serializers.SerializerMethodField()

    class Meta:
        model = Trainee
        fields = ["user", "height", "weight", "trainee_id"]

    def get_user(self, obj):
        """Fetch related user details"""
        return {
            "id": obj.user.id,
            "name": obj.user.name,
            "email": obj.user.email,
            "username": obj.user.username,
            "phone_number": obj.user.phone_number,
            "profile_picture": obj.user.profile_picture.url if obj.user.profile_picture else None,
        }
    
    def get_trainee_id(self, obj):
        return obj.id


class UpdateTraineeSerializer(serializers.ModelSerializer):
    # User fields
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    delete_profile_picture = serializers.BooleanField(required=False, write_only=True)

    user = serializers.SerializerMethodField()  # Include full user details in the response

    class Meta:
        model = Trainee
        fields = ["user", "email", "username", "name", "phone_number", "height", "weight", "profile_picture", "delete_profile_picture"]

    def get_user(self, obj):
        """Return the associated user's details in the response"""
        return {
            "name": obj.user.name,
            "email": obj.user.email,
            "username": obj.user.username,
            "phone_number": obj.user.phone_number,
            "profile_picture": obj.user.profile_picture.url if obj.user.profile_picture else None,
        }

    def validate_email(self, value):
        """Ensure the email is unique"""
        if User.objects.filter(email=value).exclude(id=self.instance.user.id).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_username(self, value):
        """Ensure the username is unique"""
        if User.objects.filter(username=value).exclude(id=self.instance.user.id).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def update(self, instance, validated_data):
        """Update both the Trainee and User models."""
        user = instance.user  # Get the related User object

        # Handle profile picture deletion
        if validated_data.get('delete_profile_picture'):
            if user.profile_picture:
                user.profile_picture.delete()  # This will delete the file from storage
            user.profile_picture = None
            validated_data.pop('delete_profile_picture')

        # Extract user-related fields from validated_data
        user_fields = ["email", "username", "phone_number", "profile_picture", "name"]
        for field in user_fields:
            if field in validated_data:
                setattr(user, field, validated_data.pop(field))  # Update user fields

        user.save()  # Save the updated User instance

        # Update remaining Trainee fields (height, weight)
        return super().update(instance, validated_data)
