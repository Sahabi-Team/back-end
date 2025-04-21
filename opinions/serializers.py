from rest_framework import serializers
from .models import Opinion

class OpinionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opinion
        fields = ['id', 'user', 'text', 'created_at']
        read_only_fields = ['user', 'created_at']
