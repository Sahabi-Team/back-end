from rest_framework import serializers
from .models import Trainer
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = ['id', 'username', 'email', 'phone_number', 'first_name', 'last_name',  'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value
