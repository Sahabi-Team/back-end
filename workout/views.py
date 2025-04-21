from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from .models import Exercise, WorkoutPlan
from .serializers import ExerciseSerializer, WorkoutPlanSerializer
from permissions.permissions import IsTrainee


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


class TraineeWorkoutPlansView(generics.ListAPIView):
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsAuthenticated, IsTrainee]

    @swagger_auto_schema(
        operation_description="List workout plans for the currently authenticated trainee."
    )
    def get_queryset(self):
        user = self.request.user
        return WorkoutPlan.objects.filter(
            trainee__user=user
        ).prefetch_related("exercises__exercise", "trainee", "trainer")
