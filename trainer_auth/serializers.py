from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Trainer
from authentication.models import User
from drf_yasg.utils import swagger_serializer_method

class TrainerSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(required=False)
    lastName = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    delete_profile_picture = serializers.BooleanField(required=False, write_only=True)

    user = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = ["user", "email", "username", "firstName", "lastName", "phone_number", "profile_picture", "delete_profile_picture", "bio", "experience", "isAvailableForReservation", "price", "specialties", "certificates"]

    @swagger_serializer_method(serializer_or_field=serializers.DictField(
        child=serializers.CharField(),
        help_text="User details including name, email, username, phone number, and profile picture URL"
    ))
    def get_user(self, obj):
        """Fetch related user details"""
        return {
            "name": obj.user.name,
            "email": obj.user.email,
            "username": obj.user.username,
            "phone_number": obj.user.phone_number,
            "profile_picture": obj.user.profile_picture.url if obj.user.profile_picture else None,
        }
    


class UpdateTrainerSerializer(serializers.ModelSerializer):
    # User fields
    name = serializers.CharField(
        required=False,
        help_text="Full name of the trainer"
    )
    email = serializers.EmailField(
        required=False,
        help_text="Email address of the trainer"
    )
    username = serializers.CharField(
        required=False,
        help_text="Username for the trainer's account"
    )
    phone_number = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Contact phone number"
    )
    profile_picture = serializers.ImageField(
        required=False,
        allow_null=True,
        help_text="Profile picture file"
    )
    delete_profile_picture = serializers.BooleanField(
        required=False,
        write_only=True,
        help_text="Set to true to delete the current profile picture"
    )

    class Meta:
        model = Trainer
        fields = ["email", "username", "name", "phone_number", "bio", "experience", 
                 "isAvailableForReservation", "price", "specialties", "certificates", 
                 "profile_picture", "delete_profile_picture"]

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
        """Update both the Trainer and User models."""
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

        # Update remaining Trainer fields
        return super().update(instance, validated_data)

    @swagger_serializer_method(serializer_or_field=serializers.DictField(
        child=serializers.CharField(),
        help_text="User details including name, email, username, phone number, and profile picture URL"
    ))
    def to_representation(self, instance):
        """Custom representation to include user details in the response"""
        ret = super().to_representation(instance)
        ret['user'] = {
            "name": instance.user.name,
            "email": instance.user.email,
            "username": instance.user.username,
            "phone_number": instance.user.phone_number,
            "profile_picture": instance.user.profile_picture.url if instance.user.profile_picture else None,
        }
        return ret


class TrainerPublicProfileSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='trainer.firstName')
    lastName = serializers.CharField(source='trainer.lastName')
    email = serializers.EmailField(source='user.email')
    profile_picture = serializers.ImageField(source='user.profile_picture')
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = ['firstName', 'lastName', 'email', 'profile_picture', 'rating']

    def get_rating(self, obj):
        return obj.rating

