from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Exercise
from .serializers import ExerciseSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ExerciseFilter
from drf_yasg.utils import swagger_auto_schema

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
    """API View to fetch exercises with filtering"""
    queryset = Exercise.objects.all().prefetch_related('tags', 'images')
    serializer_class = ExerciseSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExerciseFilter

    @swagger_auto_schema(
        operation_description="Returns a list of exercises filtered by muscle_group, difficulty, equipment, or tags."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)