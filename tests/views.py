from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Test
from .serializers import TestSerializer
from client_auth.models import Trainee
from trainer_auth.models import Trainer
from django.db.models import Max
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import timedelta
from django.utils import timezone

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

class TrainerPupilTestsView(APIView):
    """
    API for trainers to get the latest body test results for their pupils.
    Returns the most recent test for each trainee under the trainer's mentorship.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get the latest body test results for all active trainees under the trainer's mentorship",
        responses={
            200: TestSerializer(many=True),
            403: "Permission Denied - Only trainers can access this endpoint",
            401: "Authentication credentials were not provided"
        },
        tags=['tests']
    )
    def get(self, request):
        # Ensure the user is a Trainer
        try:
            trainer = request.user.trainer_profile
        except Trainer.DoesNotExist:
            return Response({"error": "Only trainers can access this endpoint."}, status=403)

        # Get all trainees under this trainer's mentorship
        trainees = Trainee.objects.filter(
            mentorships__trainer=trainer,
            mentorships__is_active=True
        ).distinct()

        # Get the latest test for each trainee
        latest_tests = []
        for trainee in trainees:
            latest_test = Test.objects.filter(trainee=trainee).order_by('-created_at').first()
            if latest_test:
                latest_tests.append(latest_test)

        serializer = TestSerializer(latest_tests, many=True, context={'request': request})
        return Response(serializer.data)

class LastTestCheckView(APIView):
    """
    API to check if a client has taken a test within the last month and get their last test date.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Check if a client has taken a test within the last month and get their last test date",
        responses={
            200: openapi.Response(
                description="Test status and last test date",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'has_test_in_last_month': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'last_test_date': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                    }
                )
            ),
            403: "Permission Denied - Only trainees can access this endpoint",
            401: "Authentication credentials were not provided"
        },
        tags=['tests']
    )
    def get(self, request):
        # Ensure the user is a Trainee
        try:
            trainee = request.user.trainee_profile
        except Trainee.DoesNotExist:
            return Response({"error": "Only trainees can access this endpoint."}, status=403)

        # Get the last test for the trainee
        last_test = Test.objects.filter(trainee=trainee).order_by('-created_at').first()

        if not last_test:
            return Response({
                'has_test_in_last_month': False,
                'last_test_date': None
            })

        # Check if the last test was within the last month
        one_month_ago = timezone.now() - timedelta(days=30)
        has_test_in_last_month = last_test.created_at >= one_month_ago

        return Response({
            'has_test_in_last_month': has_test_in_last_month,
            'last_test_date': last_test.created_at
        })
