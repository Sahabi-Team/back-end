# Django imports
from django_filters.rest_framework import DjangoFilterBackend

# DRF imports
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    ListAPIView
)
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

# Swagger (drf_yasg) imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Local app imports
from .models import Trainer
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Trainer, Comment
from .serializers import (
    TrainerSerializer,
    UpdateTrainerSerializer,
    TrainerPublicProfileSerializer,
    CommentSerializer
)
from client_auth.models import Trainee
from client_auth.serializers import TraineeSerializer
from workout.models import WorkoutPlan
from permissions.permissions import IsTrainer, IsTrainee
from django.shortcuts import get_object_or_404
from authentication.models import User
from workout.models import Mentorship

class TrainerDetailView(generics.RetrieveAPIView):
    serializer_class = TrainerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.trainer_profile

    @swagger_auto_schema(
        operation_description="Get trainer profile details",
        responses={
            200: TrainerSerializer,
            404: "Trainer profile not found"
        }
    )
    def get(self, request, *args, **kwargs):
        trainer = self.get_object()
        if trainer is None:
            return Response(
                {"message": "Trainer profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(trainer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateTrainerView(RetrieveUpdateAPIView):
    """
    get:
    Retrieve the authenticated trainer's profile details.
    
    put:
    Update the authenticated trainer's profile.
    
    patch:
    Partially update the authenticated trainer's profile.
    
    All fields are optional. You can update any combination of:
    - User details (name, email, username, phone_number, profile_picture)
    - Trainer details (bio, experience, isAvailableForReservation, price, specialties, certificates)
    """
    serializer_class = UpdateTrainerSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        """Ensure only the logged-in trainer can update their info."""
        return self.request.user.trainer_profile  # Access trainer via related_name

    @swagger_auto_schema(
        operation_description="Get trainer profile details",
        responses={
            200: UpdateTrainerSerializer,
            404: "Trainer profile not found"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update trainer profile",
        request_body=UpdateTrainerSerializer,
        responses={
            200: UpdateTrainerSerializer,
            400: "Invalid data provided",
            404: "Trainer profile not found"
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update trainer profile",
        request_body=UpdateTrainerSerializer,
        responses={
            200: UpdateTrainerSerializer,
            400: "Invalid data provided",
            404: "Trainer profile not found"
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

class TrainerTraineesView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTrainer]

    def get(self, request):
        trainer = request.user.trainer_profile 
        trainee_ids = Mentorship.objects.filter(trainer=trainer).values_list('trainee', flat=True).distinct()
        trainees = Trainee.objects.filter(id__in=trainee_ids)
        serializer = TraineeSerializer(trainees, many=True)
        return Response(serializer.data)


class FilteredTrainerListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Trainer.objects.all()
    serializer_class = TrainerPublicProfileSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['expertise']
    ordering_fields = ['experience_years', 'rating']


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTrainee]

    def perform_create(self, serializer):
        trainee = self.request.user.trainee_profile
        serializer.save(trainee=trainee)


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        trainer_id = self.kwargs.get('trainer_id')
        return Comment.objects.filter(trainer__id=trainer_id)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTrainee]

    def get_queryset(self):
        return Comment.objects.filter(trainee__user=self.request.user)
class GetTrainerIdByUsername(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        trainer = get_object_or_404(Trainer, user=user)
        return Response({'trainer_id': trainer.id}, status=status.HTTP_200_OK)
    
class GetTrainerUsernameById(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, trainer_id):
        trainer = get_object_or_404(Trainer, id=trainer_id)
        username = trainer.user.username
        return Response({'username': username}, status=status.HTTP_200_OK)
