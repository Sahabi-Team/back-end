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
    tags = ExerciseTagSerializer(many=True)
    images = ExerciseImageSerializer(many=True)

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'tags', 'muscle_groups', 'equipments', 'difficulty', 'images']


class ExerciseDetailSerializer(serializers.ModelSerializer):
    tags = ExerciseTagSerializer(many=True)
    images = ExerciseImageSerializer(many=True)

    class Meta:
        model = Exercise
        fields = [
            'id',
            'name',
            'description',
            'tags',
            'muscle_groups',
            'equipments',
            'difficulty',
            'images',
        ]


