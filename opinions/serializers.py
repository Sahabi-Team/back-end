from rest_framework import serializers
from .models import Opinion

class OpinionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Opinion
        fields = ['id', 'user', 'text', 'rating', 'created_at', 'name']
        read_only_fields = ['user', 'created_at', 'name']
