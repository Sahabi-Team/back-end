from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Test
from .serializers import TestSerializer
from client_auth.models import Trainee

class TestCreateView(generics.CreateAPIView):
    """
    API to allow a Trainee to submit a test.
    The trainee is automatically assigned based on the authenticated user.
    """
    serializer_class = TestSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure the user is a Trainee
        try:
            trainee = self.request.user.trainee_profile
        except Trainee.DoesNotExist:
            return Response({"error": "Only trainees can submit tests."}, status=403)

        # Save the Test and link it to the Trainee
        serializer.save(trainee=trainee)


class TestListView(generics.ListAPIView):
    """
    API to allow a Trainee to list all their submitted tests.
    Only the logged-in user can see their own tests.
    """
    serializer_class = TestSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            trainee = self.request.user.trainee_profile
            return Test.objects.filter(trainee=trainee).order_by("-created_at")  # Show latest tests first
        except Trainee.DoesNotExist:
            return Test.objects.none()  # If the user is not a trainee, return empty list
