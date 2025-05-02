from rest_framework import serializers
from .models import Trainer, Comment
from authentication.models import User
from drf_yasg.utils import swagger_serializer_method

class TrainerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    delete_profile_picture = serializers.BooleanField(required=False, write_only=True)
    rating = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = [
            "user", "email", "username", "first_name", "last_name", 
            "phone_number", "profile_picture", "delete_profile_picture", 
            "bio", "experience", "isAvailableForReservation", 
            "price", "specialties", "certificates", "rating"
        ]

    @swagger_serializer_method(serializer_or_field=serializers.DictField(
        child=serializers.CharField(),
        help_text="User details including name, email, username, phone number, and profile picture URL"
    ))
    def get_user(self, obj):
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "email": obj.user.email,
            "username": obj.user.username,
            "phone_number": obj.user.phone_number,
            "profile_picture": obj.user.profile_picture.url if obj.user.profile_picture else None,
        }

    def get_rating(self, obj):
        # Here we get the annotated rating from the queryset, which was added in the view
        return obj.rating if hasattr(obj, 'rating') else None
class UpdateTrainerSerializer(serializers.ModelSerializer):
    # User fields
    first_name = serializers.CharField(
        required=False,
        help_text="Full name of the trainer"
    )
    last_name = serializers.CharField(
        required=False,
        help_text="Last name of the trainer"
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
        fields = ["email", "username", "phone_number", "bio", "experience", "first_name", "last_name",
                 "isAvailableForReservation", "price", "specialties", "certificates", 
                 "profile_picture", "delete_profile_picture"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(id=self.instance.user.id).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_username(self, value):
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
        user_fields = ["email", "username", "phone_number", "profile_picture", "first_name", "last_name"]
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
            "first_name": instance.user.first_name,
            "last_name": instance.user.last_name,
            "email": instance.user.email,
            "username": instance.user.username,
            "phone_number": instance.user.phone_number,
            "profile_picture": instance.user.profile_picture.url if instance.user.profile_picture else None,
        }
        return ret


class TrainerPublicProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='trainer.last_name')
    email = serializers.EmailField(source='user.email')
    profile_picture = serializers.ImageField(source='user.profile_picture')
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = ['first_name', 'last_name', 'email', 'profile_picture', 'rating']

    def get_rating(self, obj):
        return obj.rating


class CommentSerializer(serializers.ModelSerializer):
    trainee_name = serializers.CharField(source='trainee.user.name', read_only=True)
    trainee_email = serializers.EmailField(source='trainee.user.email', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'trainee_name', 'trainee_email', 'trainer', 'comment', 'rating', 'created_at']
        read_only_fields = ['trainee_name', 'trainee_email', 'created_at']
