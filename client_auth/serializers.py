from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Trainee
from authentication.models import User

class TraineeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Trainee
        fields = ["user", "height", "weight"]

    def get_user(self, obj):
        """Fetch related user details"""
        return {
            "email": obj.user.email,
            "username": obj.user.username,
            "phone_number": obj.user.phone_number,
        }
    


class UpdateTraineeSerializer(serializers.ModelSerializer):
    # User fields
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False, allow_blank=True)

    user = serializers.SerializerMethodField()  # Include full user details in the response

    class Meta:
        model = Trainee
        fields = ["user", "email", "username", "phone_number", "height", "weight"]

    def get_user(self, obj):
        """Return the associated user's details in the response"""
        return {
            "email": obj.user.email,
            "username": obj.user.username,
            "phone_number": obj.user.phone_number,
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

        # Extract user-related fields from validated_data
        user_fields = ["email", "username", "phone_number"]
        for field in user_fields:
            if field in validated_data:
                setattr(user, field, validated_data.pop(field))  # Update user fields

        user.save()  # Save the updated User instance

        # Update remaining Trainee fields (height, weight)
        return super().update(instance, validated_data)
