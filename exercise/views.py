from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Exercise
from .serializers import ExerciseSerializer

class ExerciseListView(generics.ListAPIView):
    """API View to fetch all exercises"""
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [AllowAny]  # Public API
