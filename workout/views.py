from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Exercise
from .serializers import ExerciseSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ExerciseListView(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['muscle_group', 'difficulty', 'equipment']

    @swagger_auto_schema(
        operation_description="List exercises with optional filtering by muscle group, difficulty, or equipment."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)