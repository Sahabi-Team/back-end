from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Test
from .serializers import TestSerializer

class SubmitTestView(generics.CreateAPIView):
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Ensure the test is saved and associated with the trainee"""
        user = self.request.user

        # Check if user has a trainee profile
        if not hasattr(user, 'trainee'):
            return Response({"error": "Only trainees can submit test results."}, status=status.HTTP_403_FORBIDDEN)

        trainee = user.trainee
        test = serializer.save(trainee=trainee)  

        # Debugging logs
        print(f"Test created for trainee {trainee.id}: {test}")
