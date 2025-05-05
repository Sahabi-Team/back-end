from rest_framework import serializers
from .models import Exercise, ExerciseImage, ExerciseTag, MuscleGroup, Equipment
from django.conf import settings


class ProductionImageField(serializers.ImageField):
    def to_representation(self, value):
        if not value:
            return None
        url = value.url
        return f"{settings.PRODUCTION_DOMAIN}{url}"


class ExerciseImageSerializer(serializers.ModelSerializer):
    image = ProductionImageField()

    class Meta:
        model = ExerciseImage
        fields = ['image']


class ExerciseTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseTag
        fields = ['name']


class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = ['name']


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['name']


class ExerciseSerializer(serializers.ModelSerializer):
    tags = ExerciseTagSerializer(many=True, read_only=True)
    images = ExerciseImageSerializer(many=True, read_only=True)
    muscle_groups = MuscleGroupSerializer(many=True, read_only=True)
    equipments = EquipmentSerializer(many=True, read_only=True)
    workoutplaces_display = serializers.CharField(source='get_workoutplaces_display', read_only=True)

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
            'workoutplaces',
            'workoutplaces_display',
            'images',
        ]
