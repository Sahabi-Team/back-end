from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Exercise
from .serializers import ExerciseSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ExerciseFilter
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from drf_yasg import openapi

class ExerciseListView(generics.ListAPIView):
    """API View to fetch all exercises"""
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Returns a list of all exercises."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FilteredExerciseListView(generics.ListAPIView):
    queryset = Exercise.objects.all().prefetch_related('tags', 'images')
    serializer_class = ExerciseSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ExerciseFilter
    search_fields = ['name']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('tags', openapi.IN_QUERY, description="Comma-separated tag names", type=openapi.TYPE_STRING),
            openapi.Parameter('muscle_group', openapi.IN_QUERY, description="Comma-separated muscle groups", type=openapi.TYPE_STRING),
            openapi.Parameter('difficulty', openapi.IN_QUERY, description="Comma-separated difficulty levels", type=openapi.TYPE_STRING),
            openapi.Parameter('equipment', openapi.IN_QUERY, description="Comma-separated equipment names", type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by name", type=openapi.TYPE_STRING),
        ],
        operation_description="Returns a list of exercises filtered by muscle group, difficulty, equipment, tags, or searched by name."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)