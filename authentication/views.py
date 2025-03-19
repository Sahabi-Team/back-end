from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class UserDetailView(CreateAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
