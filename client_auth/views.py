from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Trainee
from .serializers import TraineeSerializer, UpdateTraineeSerializer

class TraineeDetailView(RetrieveAPIView):
    serializer_class = TraineeSerializer
    permission_classes = [IsAuthenticated]  # Ensure JWT authentication is required

    def get_object(self):
        """Ensure that a user can only access their own trainee profile"""
        user = self.request.user
        try:
            return user.trainee_profile  # Fetch the trainee linked to this user
        except Trainee.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        trainee = self.get_object()
        if trainee is None:
            return Response(
                {"message": "Trainee profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(trainee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def get(self, request, *args, **kwargs):
        trainee = self.get_object()
        if trainee is None:
            return Response(
                {"message": "Trainee profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(trainee)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateTraineeView(RetrieveUpdateAPIView):
    serializer_class = UpdateTraineeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Ensure only the logged-in trainee can update their info."""
        return self.request.user.trainee_profile  # Access trainee via related_name
