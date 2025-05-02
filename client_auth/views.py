from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Trainee
from .serializers import TraineeSerializer, UpdateTraineeSerializer
from rest_framework import status, generics, permissions
from django.shortcuts import get_object_or_404
from authentication.models import User

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
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        """Ensure only the logged-in trainee can update their info."""
        return self.request.user.trainee_profile  # Access trainee via related_name


class GetTraineeIdByUsername(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        trainee = get_object_or_404(Trainee, user=user)
        return Response({'trainee_id': trainee.id}, status=status.HTTP_200_OK)
    
class GetTraineeUsernameById(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, trainee_id):
        trainee = get_object_or_404(Trainee, id=trainee_id)
        username = trainee.user.username
        return Response({'username': username}, status=status.HTTP_200_OK)
