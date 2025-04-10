from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from trainer_auth.models import Trainer 
from client_auth.models import Trainee
from exercise.models import Exercise
from workout.models import WorkoutPlan
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class TotalClientsView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Get Total Clients",
        operation_description="Returns the total number of registered clients (Trainees).",
        responses={200: openapi.Response(description="Number of clients")}
    )
    def get(self, request):
        return Response({"total_clients": Trainee.objects.count()})


class TotalTrainersView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Get Total Trainers",
        operation_description="Returns the total number of registered trainers.",
        responses={200: openapi.Response(description="Number of trainers")}
    )
    def get(self, request):
        return Response({"total_trainers": Trainer.objects.count()})


class TotalWorkoutPlansView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Get Total Workout Plans",
        operation_description="Returns the total number of created workout plans.",
        responses={200: openapi.Response(description="Number of workout plans")}
    )
    def get(self, request):
        return Response({"total_workout_plans": WorkoutPlan.objects.count()})


class TotalExercisesView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Get Total Exercises",
        operation_description="Returns the total number of exercises available.",
        responses={200: openapi.Response(description="Number of exercises")}
    )
    def get(self, request):
        return Response({"total_exercises": Exercise.objects.count()})

