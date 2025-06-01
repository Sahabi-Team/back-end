# Django imports
from django.db.models import Q, Avg, FloatField, Value
from django.db.models.functions import Coalesce
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

# Third-party imports
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# DRF imports
from rest_framework import status, generics, permissions, filters
from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# Local app imports
from .models import Trainer, Comment
from .serializers import (
    TrainerSerializer,
    UpdateTrainerSerializer,
    TrainerPublicProfileSerializer,
    CommentSerializer
)
from client_auth.models import Trainee
from client_auth.serializers import TraineeSerializer
from workout.models import WorkoutPlan, Mentorship
from authentication.models import User
from permissions.permissions import IsTrainer, IsTrainee

class TrainerDetailView(generics.RetrieveAPIView):
    serializer_class = TrainerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.trainer_profile
        except ObjectDoesNotExist:
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
    permission_classes = [permissions.IsAuthenticated, IsTrainer]

    def get(self, request):
        trainer = request.user.trainer_profile 
        trainee_ids = Mentorship.objects.filter(trainer=trainer).values_list('trainee', flat=True).distinct()
        trainees = Trainee.objects.filter(id__in=trainee_ids)
        
        # Get all trainee data from serializer
        trainee_data = TraineeSerializer(trainees, many=True).data
        
        # Add status to each trainee's data
        for i, trainee in enumerate(trainees):
            mentorship = Mentorship.objects.filter(trainer=trainer, trainee=trainee).first()
            has_workout_plan = WorkoutPlan.objects.filter(mentorship=mentorship).exists()
            status = 'تکمیل شده' if has_workout_plan else 'در انتظار'
            trainee_data[i]['status'] = status
            
        return Response(trainee_data)


class FilteredTrainerListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TrainerSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['experience', 'avg_rating', 'isAvailableForReservation']
    search_fields = ['user__name', 'user__username', 'user__first_name', 'user__last_name']
    ordering = ['-isAvailableForReservation']  # Default ordering: available trainers first

    @swagger_auto_schema(
        operation_description="Retrieve a list of trainers filtered by various parameters.",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Search for a trainer by name, username, first name, or last name.", type=openapi.TYPE_STRING),
            openapi.Parameter('specialties', openapi.IN_QUERY, description="Comma-separated list of specialties to filter by.", type=openapi.TYPE_STRING),
            openapi.Parameter('experience', openapi.IN_QUERY, description="Experience range(s) in the format 'min-max', e.g., '2-5,6-10'.", type=openapi.TYPE_STRING),
            openapi.Parameter('rating', openapi.IN_QUERY, description="Comma-separated list of ratings to filter by.", type=openapi.TYPE_STRING),
            openapi.Parameter('price_min', openapi.IN_QUERY, description="Minimum price filter.", type=openapi.TYPE_NUMBER),
            openapi.Parameter('price_max', openapi.IN_QUERY, description="Maximum price filter.", type=openapi.TYPE_NUMBER),
            openapi.Parameter('available', openapi.IN_QUERY, description="Filter by availability (true/false).", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by field(s). Prefix with '-' for descending order. Available fields: experience, avg_rating, isAvailableForReservation", type=openapi.TYPE_STRING),
        ],
        responses={
            200: TrainerSerializer(many=True),
            400: openapi.Response('Bad Request'),
            404: openapi.Response('Not Found'),
        }
    )
    def get_queryset(self):
        queryset = Trainer.objects.all()
        params = self.request.query_params
        from django.db.models import Avg, F, ExpressionWrapper, Value,IntegerField
        from django.db.models.functions import Floor,Round
        queryset = queryset.annotate(
            avg_rating=Round(Avg('comments_received__rating'), 1)
        )

        queryset = queryset.annotate(
            ratingg=Floor('avg_rating')
        )
        
        search = params.get('search')
        if search:
            queryset = queryset.filter(
                Q(user__name__icontains=search) |
                Q(user__username__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )

        # Filter by specialties
        specialities = params.get('specialties')
        if specialities:
            speciality_list = [s.strip() for s in specialities.split(',')]
            queryset = queryset.filter(specialties__in=speciality_list).distinct()

        # Filter by experience
        experience = params.get('experience')
        if experience:
            experience_ranges = [e.strip() for e in experience.split(',')]
            experience_q = Q()
            for exp_range in experience_ranges:
                try:
                    low, high = map(int, exp_range.split('-'))
                    experience_q |= Q(experience__gte=low, experience__lte=high)
                except ValueError:
                    continue
            queryset = queryset.filter(experience_q)

        # Filter by rating
        # print(queryset[0].__dict__)
        rating = params.get('rating')
        if rating:
            # print(rating,"777")
            try:
                rating_values = min([float(r.strip()) for r in rating.split(',')])
                queryset = queryset.filter(ratingg__gte=rating_values)
            except ValueError:
                pass

        # Filter by price minimum
        price_min = params.get('price_min')
        if price_min:
            try:
                queryset = queryset.filter(price__gte=float(price_min))
            except ValueError:
                pass

        # Filter by price maximum
        price_max = params.get('price_max')
        if price_max:
            try:
                queryset = queryset.filter(price__lte=float(price_max))
            except ValueError:
                pass

        # Filter by availability
        available = params.get('available')
        if available and available.lower() == 'true':
            queryset = queryset.filter(isAvailableForReservation=True)

        return queryset.distinct()


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
class TrainerPublicProfileView(APIView):
    authentication_classes = []  # No authentication
    permission_classes = []      # No permission checks

    def get(self, request, trainer_id):
        try:
            trainer = Trainer.objects.get(id=trainer_id)
        except Trainer.DoesNotExist:
            return Response({'error': 'Trainer not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TrainerPublicProfileSerializer(trainer)
        return Response(serializer.data, status=status.HTTP_200_OK)