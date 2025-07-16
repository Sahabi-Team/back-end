from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from .models import Mentorship
from .serializers import MentorshipSerializer, MentorshipCreateSerializer
from trainer_auth.models import Trainer
from django.shortcuts import get_object_or_404
from workout.serializers import WorkoutPlanSerializer
# Create your views here.
from workout.models import WorkoutPlan

class IsTraineeOrTrainer(permissions.BasePermission):
    """
    Custom permission to only allow trainees to create mentorships
    and both trainees and trainers to view their own mentorships.
    """
    def has_permission(self, request, view):
        # Allow trainees to create mentorships
        if request.method == 'POST' and hasattr(request.user, 'trainee_profile'):
            return True
        
        # Allow both trainees and trainers to view mentorships
        return request.method in permissions.SAFE_METHODS and (
            hasattr(request.user, 'trainee_profile') or 
            hasattr(request.user, 'trainer_profile')
        )
    
    def has_object_permission(self, request, view, obj):
        # Allow trainees to view their own mentorships
        if hasattr(request.user, 'trainee_profile'):
            return obj.trainee == request.user.trainee_profile
        
        # Allow trainers to view mentorships where they are the trainer
        if hasattr(request.user, 'trainer_profile'):
            return obj.trainer == request.user.trainer_profile
        
        return False

class MentorshipViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing mentorship connections.
    """
    serializer_class = MentorshipSerializer
    permission_classes = [permissions.IsAuthenticated, IsTraineeOrTrainer]
    http_method_names = ['get', 'post', 'patch', 'delete']  # Disable PUT

    def get_queryset(self):
        """
        This view should return a list of all mentorship connections
        for the currently authenticated user.
        """
        user = self.request.user
        
        # If user is a trainer, return mentorships where they are the trainer
        if hasattr(user, 'trainer_profile'):
            return Mentorship.objects.filter(trainer=user.trainer_profile)
        
        # If user is a trainee, return mentorships where they are the trainee
        elif hasattr(user, 'trainee_profile'):
            return Mentorship.objects.filter(trainee=user.trainee_profile)
        
        # If user is neither, return empty queryset
        return Mentorship.objects.none()

    def get_serializer_class(self):
        """
        Return different serializers for different actions.
        """
        if self.action == 'create':
            return MentorshipCreateSerializer
        return MentorshipSerializer

    def perform_create(self, serializer):
        """
        Override perform_create to associate the mentorship with the current trainee.
        """
        user = self.request.user
        if not hasattr(user, 'trainee_profile'):
            raise PermissionDenied("Only trainees can create mentorship connections.")
        
        # Check if a mentorship already exists with this trainer
        trainer = serializer.validated_data['trainer']
        if Mentorship.objects.filter(trainee=user.trainee_profile, trainer=trainer, is_active=True).exists():
            raise PermissionDenied("You already have an active mentorship with this trainer.")
        
        serializer.save(trainee=user.trainee_profile)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """
        Toggle the active status of a mentorship connection.
        """
        mentorship = self.get_object()
        mentorship.is_active = not mentorship.is_active
        mentorship.save()
        return Response({'status': 'active status toggled'})

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get all active mentorship connections for the current user.
        """
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def expired(self, request):
        """
        Get all expired mentorship connections for the current user.
        """
        queryset = self.get_queryset().filter(is_active=True)
        expired_mentorships = [m for m in queryset if m.is_expired()]
        serializer = self.get_serializer(expired_mentorships, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=['get'], url_path='last_workout_plan')
    def last_workout_plan(self, request, pk=None):
        """
        Retrieve the most recent workout plan associated with this mentorship.
        """
        mentorship = self.get_object()

        last_plan = mentorship.workout_plans.order_by('-created_at').first()
        if not last_plan:
            return Response(
                {"detail": "No workout plans found for this mentorship."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = WorkoutPlanSerializer(last_plan)
        return Response(serializer.data)