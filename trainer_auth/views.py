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
from .serializers import (
    TrainerSerializer,
    UpdateTrainerSerializer,
    TrainerPublicProfileSerializer
)
from client_auth.models import Trainee
from client_auth.serializers import TraineeSerializer
from mentorship.models import Mentorship
from permissions.permissions import IsTrainer


class TrainerDetailView(RetrieveAPIView):
    """
    get:
    Retrieve the authenticated trainer's profile details.
    
    Returns the trainer's profile information including user details, bio, experience, 
    availability, price, specialties, and certificates.
    """
    serializer_class = TrainerSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Ensure that a user can only access their own trainer profile"""
        user = self.request.user
        try:
            return user.trainer_profile  # Fetch the trainer linked to this user
        except Trainer.DoesNotExist:
            return None

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
    permission_classes = [IsAuthenticated,IsTrainer]

    def get(self, request):
        trainer = request.user.trainer_profile 
        trainee_ids = Mentorship.objects.filter(trainer=trainer).values_list('trainee', flat=True).distinct()
        trainees = Trainee.objects.filter(id__in=trainee_ids)
        serializer = TraineeSerializer(trainees, many=True)
        return Response(serializer.data)
    

class FilteredTrainerListView(ListAPIView):
    permission_classes=[AllowAny]
    queryset = Trainer.objects.all()
    serializer_class = TrainerPublicProfileSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['expertise']
    ordering_fields = ['experience_years', 'rating']

    @swagger_auto_schema(
        operation_description="Get list of trainers filtered by expertise, experience, or rating",
        manual_parameters=[
            openapi.Parameter(
                'expertise', openapi.IN_QUERY, description="Filter by expertise",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ordering', openapi.IN_QUERY,
                description="Order by experience_years or rating (use - for descending)",
                type=openapi.TYPE_STRING,
                enum=['experience_years', '-experience_years', 'rating', '-rating']
            ),
        ],
        responses={200: TrainerPublicProfileSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)