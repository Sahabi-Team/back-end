from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import WorkoutPlan, WorkoutExercise
from .serializers import WorkoutPlanSerializer, WorkoutExerciseSerializer
from mentorship.models import Mentorship
from exercise.models import Exercise
from django.db.models import Q

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
        # Get all workout plans where the user is either the trainer or trainee
        return WorkoutPlan.objects.filter(
            Q(mentorship__trainer__user=user) | Q(mentorship__trainee__user=user)
        ).select_related('mentorship', 'mentorship__trainer__user', 'mentorship__trainee__user')

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
        return WorkoutExercise.objects.filter(
            Q(workout_plan__mentorship__trainer__user=user) | Q(workout_plan__mentorship__trainee__user=user)
        ).select_related('workout_plan', 'workout_plan__mentorship', 'exercise')

    def perform_create(self, serializer):
        workout_plan_id = self.request.data.get('workout_plan_id')
        exercise_id = self.request.data.get('exercise_id')
        
        try:
            workout_plan = WorkoutPlan.objects.get(id=workout_plan_id)
            exercise = Exercise.objects.get(id=exercise_id)
            
            if workout_plan.mentorship.trainer.user != self.request.user:
                raise serializers.ValidationError("You can only add exercises to your own workout plans.")
            
            # Check if either reps or duration is provided
            if not self.request.data.get('reps') and not self.request.data.get('duration'):
                raise serializers.ValidationError("Either reps or duration must be provided.")
            
            # Check if both reps and duration are provided
            if self.request.data.get('reps') and self.request.data.get('duration'):
                raise serializers.ValidationError("Provide either reps or duration, not both.")
            
            serializer.save(workout_plan=workout_plan, exercise=exercise)
            
        except WorkoutPlan.DoesNotExist:
            raise serializers.ValidationError("Workout plan not found.")
        except Exercise.DoesNotExist:
            raise serializers.ValidationError("Exercise not found.")
