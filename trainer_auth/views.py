from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Trainer
from .serializers import TrainerSerializer, UpdateTrainerSerializer

class TrainerDetailView(RetrieveAPIView):
    serializer_class = TrainerSerializer
    permission_classes = [IsAuthenticated]  # Ensure JWT authentication is required

    def get_object(self):
        """Ensure that a user can only access their own trainer profile"""
        user = self.request.user
        try:
            return user.trainer_profile  # Fetch the trainer linked to this user
        except Trainer.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        trainer = self.get_object()
        if trainer is None:
            return Response(
                {"message": "Trainer profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(trainer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

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
    serializer_class = UpdateTrainerSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Ensure only the logged-in trainee can update their info."""
        return self.request.user.trainer_profile  # Access trainee via related_name
