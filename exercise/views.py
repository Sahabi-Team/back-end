from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Exercise
from .serializers import ExerciseSerializer
from .filters import ExerciseFilter


class ExerciseListView(generics.ListAPIView):
    """Returns a list of all exercises."""
    queryset = Exercise.objects.all().prefetch_related('tags', 'images', 'muscle_groups', 'equipments')
    serializer_class = ExerciseSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Returns a list of all exercises."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FilteredExerciseListView(generics.ListAPIView):
    """Returns a list of filtered exercises."""
    queryset = Exercise.objects.all().prefetch_related('tags', 'images', 'muscle_groups', 'equipments')
    serializer_class = ExerciseSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ExerciseFilter
    search_fields = ['name']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('tags', openapi.IN_QUERY, description="Comma-separated tag names", type=openapi.TYPE_STRING),
            openapi.Parameter('muscle_groups', openapi.IN_QUERY, description="Comma-separated muscle groups", type=openapi.TYPE_STRING),
            openapi.Parameter('difficulty', openapi.IN_QUERY, description="Comma-separated difficulty levels", type=openapi.TYPE_STRING),
            openapi.Parameter('equipments', openapi.IN_QUERY, description="Comma-separated equipment names", type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by exercise name", type=openapi.TYPE_STRING),
        ],
        operation_description="Returns a list of exercises filtered by tag, muscle group, difficulty, equipment, or searched by name."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


