from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import WorkoutPlan, WorkoutExercise
from .serializers import WorkoutPlanSerializer, WorkoutExerciseSerializer
from mentorship.models import Mentorship

class IsTrainerOfMentorship(permissions.BasePermission):
    """
    Custom permission to only allow trainers of a mentorship to edit workout plans.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the trainer of the mentorship
        return obj.mentorship.trainer.user == request.user

class WorkoutPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing workout plans.
    
    * List all workout plans for the authenticated user (trainer or trainee)
    * Create new workout plans (trainers only)
    * Retrieve, update, and delete workout plans (trainers only)
    """
    serializer_class = WorkoutPlanSerializer
    permission_classes = [permissions.IsAuthenticated, IsTrainerOfMentorship]

    @swagger_auto_schema(
        operation_description="List all workout plans for the authenticated user",
        responses={200: WorkoutPlanSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new workout plan",
        request_body=WorkoutPlanSerializer,
        responses={
            201: WorkoutPlanSerializer,
            400: "Bad Request",
            403: "Permission Denied"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'trainer'):
            # If user is a trainer, return workout plans for their mentorships
            return WorkoutPlan.objects.filter(mentorship__trainer__user=user)
        elif hasattr(user, 'trainee'):
            # If user is a trainee, return workout plans for their mentorships
            return WorkoutPlan.objects.filter(mentorship__trainee__user=user)
        return WorkoutPlan.objects.none()

    def perform_create(self, serializer):
        mentorship_id = self.request.data.get('mentorship')
        try:
            mentorship = Mentorship.objects.get(id=mentorship_id)
            if mentorship.trainer.user != self.request.user:
                raise permissions.PermissionDenied("You can only create workout plans for your own mentorships.")
            serializer.save()
        except Mentorship.DoesNotExist:
            raise serializers.ValidationError("Mentorship not found.")

    @swagger_auto_schema(
        operation_description="Add an exercise to a workout plan",
        request_body=WorkoutExerciseSerializer,
        responses={
            201: WorkoutExerciseSerializer,
            400: "Bad Request",
            403: "Permission Denied"
        }
    )
    @action(detail=True, methods=['post'])
    def add_exercise(self, request, pk=None):
        workout_plan = self.get_object()
        serializer = WorkoutExerciseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(workout_plan=workout_plan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WorkoutExerciseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing workout exercises.
    
    * List all exercises in workout plans (trainer or trainee)
    * Create, update, and delete exercises in workout plans (trainers only)
    """
    serializer_class = WorkoutExerciseSerializer
    permission_classes = [permissions.IsAuthenticated, IsTrainerOfMentorship]

    @swagger_auto_schema(
        operation_description="List all exercises in workout plans",
        responses={200: WorkoutExerciseSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new exercise in a workout plan",
        request_body=WorkoutExerciseSerializer,
        responses={
            201: WorkoutExerciseSerializer,
            400: "Bad Request",
            403: "Permission Denied"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'trainer'):
            return WorkoutExercise.objects.filter(workout_plan__mentorship__trainer__user=user)
        elif hasattr(user, 'trainee'):
            return WorkoutExercise.objects.filter(workout_plan__mentorship__trainee__user=user)
        return WorkoutExercise.objects.none()

    def perform_create(self, serializer):
        workout_plan_id = self.request.data.get('workout_plan')
        try:
            workout_plan = WorkoutPlan.objects.get(id=workout_plan_id)
            if workout_plan.mentorship.trainer.user != self.request.user:
                raise permissions.PermissionDenied("You can only add exercises to your own workout plans.")
            serializer.save()
        except WorkoutPlan.DoesNotExist:
            raise serializers.ValidationError("Workout plan not found.")
