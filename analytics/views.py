from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from trainer_auth.models import Trainer 
from client_auth.models import Trainee
from exercise.models import Exercise
from workout.models import WorkoutPlan


class TotalClientsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"total_clients": Trainee.objects.count()})


class TotalTrainersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"total_trainers": Trainer.objects.count()})


class TotalWorkoutPlansView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"total_workout_plans": WorkoutPlan.objects.count()})


class TotalExercisesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"total_exercises": Exercise.objects.count()})
