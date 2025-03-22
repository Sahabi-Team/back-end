from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Trainer, Trainee
from .serializers import TrainerSerializer, TraineeSerializer
from .authentication import JWTAuthentication
from .permissions import IsTrainer, IsTrainee
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from rest_framework.permissions import AllowAny
from .models import Trainer, Trainee
from .serializers import UserSerializer

User = get_user_model()

class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        try:
            user_type = data.get("user_type")
            print(user_type)
            if user_type not in ['trainer', 'trainee']:
                return Response({"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                phone_number=data["phone_number"],
                password=data["password"],
                user_type=user_type
            )

            if user_type == 'trainer':
                Trainer.objects.create(user=user)
            else:
                Trainee.objects.create(user=user)

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            "user_id": user.id,
            "username": user.username,
            "user_type": user.user_type,
            "exp": datetime.utcnow() + timedelta(hours=24),  
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return Response({"token": token}, status=status.HTTP_200_OK)

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Email address not found."}, status=status.HTTP_400_BAD_REQUEST)

        token = default_token_generator.make_token(user)
        print("dbg:" ,token)
        # reset_link = f"{settings.FRONTEND_URL}/reset-password/?token={token}"
        reset_link = f"http://localhost:8000/sahabiapp/reset-password/?token={token}"
        print("dbg:                             ",reset_link)

        send_mail(
            "Password Reset Request",
            f"Click on the link below to reset your password:\n{reset_link}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # print(request.)
        token = request.GET.get("token")
        new_password = request.data.get("new_password")
        email = request.data.get("email") 

        if not token or not new_password or not email:
            return Response({"error": "Email, token, and new password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)  

            if not default_token_generator.check_token(user, token):  
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)

class TrainerListCreate(generics.ListCreateAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsTrainer]

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type != 'trainer':
            raise PermissionError("You must be a trainer to create a trainer profile.")
        serializer.save(user=user)

class TraineeListCreate(generics.ListCreateAPIView):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsTrainee]

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type != 'trainee':
            raise PermissionError("You must be a trainee to create a trainee profile.")
        serializer.save(user=user)

class TrainerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsTrainer]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionError("You can only access your own profile.")
        return obj

class TraineeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsTrainee]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionError("You can only access your own profile.")
        return obj
