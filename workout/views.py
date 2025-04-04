from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Exercise
from .serializers import ExerciseSerializer

class ExerciseListView(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['muscle_group', 'difficulty', 'equipment']
