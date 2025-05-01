from rest_framework import serializers
from .models import Trainer, Comment
from authentication.models import User

class TrainerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = ["user", "expertise", "experience_years"]

    def get_user(self, obj):
        return {
            "name": obj.user.name,
            "email": obj.user.email,
            "username": obj.user.username,
            "phone_number": obj.user.phone_number,
            "profile_picture": obj.user.profile_picture.url if obj.user.profile_picture else None,
        }


class UpdateTrainerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = ["user", "email", "username", "phone_number", "expertise", "experience_years"]

    def get_user(self, obj):
        return {
            "email": obj.user.email,
            "username": obj.user.username,
            "phone_number": obj.user.phone_number,
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(id=self.instance.user.id).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exclude(id=self.instance.user.id).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def update(self, instance, validated_data):
        user = instance.user
        for field in ["email", "username", "phone_number"]:
            if field in validated_data:
                setattr(user, field, validated_data.pop(field))
        user.save()
        return super().update(instance, validated_data)


class TrainerPublicProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name')
    email = serializers.EmailField(source='user.email')
    profile_picture = serializers.ImageField(source='user.profile_picture')
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = ['name', 'email', 'profile_picture', 'expertise', 'experience_years', 'rating']

    def get_rating(self, obj):
        return obj.rating


class CommentSerializer(serializers.ModelSerializer):
    trainee_name = serializers.CharField(source='trainee.user.name', read_only=True)
    trainee_email = serializers.EmailField(source='trainee.user.email', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'trainee_name', 'trainee_email', 'trainer', 'comment', 'rating', 'created_at']
        read_only_fields = ['trainee_name', 'trainee_email', 'created_at']
