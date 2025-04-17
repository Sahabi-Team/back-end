from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from .models import User
from .serializers import (
    RegisterSerializer, UserSerializer, ChangePasswordSerializer,
    PasswordResetRequestSerializer, PasswordResetSerializer
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: "User registered successfully", 400: "Validation failed"}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully!",
                "user": {
                    "email": user.email,
                    "username": user.username
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "Registration failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login with username and password (not email)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: "Login successful", 401: "Invalid credentials"}
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get("username", None)
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if (not email and not username) or not password:
            return Response(
                {"message": "credentials are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not username:
            user = authenticate(request, email=email, password=password)
            return Response(
                {"message": "GIMME USERNAME NOT EMAIL! BE HABIB BEGOO DOROST KONE IN GHESMATO KE BA EMAIL HAM BESHE LOGIN KARD!"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"message": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        response = super().post(request, *args, **kwargs)
        return Response(
            {
                "message": "Login successful",
                "tokens": response.data
            },
            status=status.HTTP_200_OK
        )


class UserDetailView(CreateAPIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        responses={200: UserSerializer}
    )
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        responses={200: "Password updated successfully", 400: "Validation error"}
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = request.user
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()

            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):

    @swagger_auto_schema(
        request_body=PasswordResetRequestSerializer,
        responses={200: "Password reset link sent to your email.", 400: "Validation error"}
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):

    @swagger_auto_schema(
        request_body=PasswordResetSerializer,
        responses={200: "Password reset successful!", 400: "Token invalid or expired"}
    )
    def post(self, request, uid, token):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uid, token)
            return Response({"message": "Password reset successful!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WhoAmI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # profile = user.get_profile()
        data = {
            "username": user.username,
            "email": user.email,
            "usertype": user.usertype,
            "first_name": user.name,
            "phone_number": user.phone_number,
            "profile_picture": user.profile_picture.url if user.profile_picture else None,
        }

        # if profile:
        #     data["profile"] = {
        #         key: getattr(profile, key)
        #         for key in profile._meta.fields_map.keys()
        #         if hasattr(profile, key)
        #     }

        return Response(data)


class UpdateProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="Update user's profile picture",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'profile_picture': openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description='Profile picture file'
                ),
            },
        ),
        responses={200: "Profile picture updated successfully", 400: "Invalid request"}
    )
    def post(self, request):
        if 'profile_picture' not in request.FILES:
            return Response(
                {"error": "No profile picture provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = request.user
        user.profile_picture = request.FILES['profile_picture']
        user.save()
        
        return Response({
            "message": "Profile picture updated successfully",
            "profile_picture_url": request.build_absolute_uri(user.profile_picture.url)
        }, status=status.HTTP_200_OK)
