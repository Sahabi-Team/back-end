from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from .models import User
from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # Validate the serializer
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully!",
                "user": {
                    "email": user.email,
                    "username": user.username
                }
            }, status=status.HTTP_201_CREATED)

        # If serializer is invalid, return custom error messages
        return Response({
            "message": "Registration failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]  # Allow anyone to attempt login

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
            print(user,username,password)
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

        response = super().post(request, *args, **kwargs)  # Call TokenObtainPairView

        return Response(
            {
                "message": "Login successful",
                "tokens": response.data  # Include the JWT tokens
            },
            status=status.HTTP_200_OK
        )


class UserDetailView(CreateAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication (JWT)

    def post(self, request):
        """Handle the password change request."""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = request.user
            new_password = serializer.validated_data['new_password']

            # Set the new password
            user.set_password(new_password)
            user.save()

            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PasswordResetRequestView(APIView):
#     def post(self, request):
#         serializer = PasswordResetRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             user = User.objects.get(email=email)

#             # Generate password reset token
#             uidb64 = urlsafe_base64_encode(force_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)
#             reset_link = f"http://localhost:8000/api/auth/password-reset-confirm/{uidb64}/{token}/"

#             # Send email
#             send_mail(
#                 subject="Password Reset Request",
#                 message=f"Click the link to reset your password: {reset_link}",
#                 from_email=settings.EMAIL_HOST_USER,
#                 recipient_list=[email],
#                 fail_silently=False,
#             )

#             return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PasswordResetConfirmView(APIView):
#     def post(self, request, uidb64, token):
#         serializer = PasswordResetConfirmSerializer(data={**request.data, "uidb64": uidb64, "token": token})
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
