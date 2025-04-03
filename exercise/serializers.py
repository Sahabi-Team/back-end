from rest_framework import serializers
from .models import Exercise, ExerciseImage, ExerciseTag

class ExerciseImageSerializer(serializers.ModelSerializer):
    """Serializer for Exercise images"""
    class Meta:
        model = ExerciseImage
        fields = ['id', 'image']

class ExerciseTagSerializer(serializers.ModelSerializer):
    """Serializer for Exercise tags"""
    class Meta:
        model = ExerciseTag
        fields = ['id', 'name']

class ExerciseSerializer(serializers.ModelSerializer):
    """Serializer for Exercise with images & tags"""
    images = ExerciseImageSerializer(many=True, read_only=True)  # Include all images
    tags = ExerciseTagSerializer(many=True, read_only=True)  # Include tag names

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'tags', 'images']
