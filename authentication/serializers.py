from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from client_auth.models import Trainee
# from trainer.models import Trainer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)

        # Create related profiles (Trainee or Trainer)
        if validated_data.get("is_trainee"):
            Trainee.objects.create(user=user)
        # elif validated_data.get("is_trainer"):
        #     Trainer.objects.create(user=user)

        return user
