from rest_framework import serializers
from .models import Exercise, ExerciseImage, ExerciseTag, MuscleGroup, Equipment


class ExerciseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseImage
        fields = ['id', 'image']


class ExerciseTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseTag
        fields = ['id', 'name']


class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = ['id', 'name']


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name']


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
