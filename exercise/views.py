from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Exercise
from .serializers import ExerciseSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ExerciseFilter

class ExerciseListView(generics.ListAPIView):
    """API View to fetch all exercises"""
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [AllowAny]  # Public API


class FilteredExerciseListView(generics.ListAPIView):
    """API View to fetch exercises with filtering"""
    queryset = Exercise.objects.all().prefetch_related('tags', 'images')
    serializer_class = ExerciseSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExerciseFilter