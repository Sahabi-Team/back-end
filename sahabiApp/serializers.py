from rest_framework import serializers
from .models import User, Trainer, Trainee

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'user_type']

class TrainerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trainer
        fields = ['user', 'expertise', 'certifications', 'experience_years']

class TraineeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trainee
        fields = ['user', 'age', 'enrolled_courses']
