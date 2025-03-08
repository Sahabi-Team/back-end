from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Trainer
from .serializers import TrainerSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password,check_password
from trainer_auth.models import Trainer


@api_view(['POST'])
def trainer_signup(request):
    if request.method == 'POST':
        serializer = TrainerSerializer(data=request.data)
        # print("sxxx",serializer)
        if serializer.is_valid():
            # print(serializer.validated_data['password'])
            password = make_password(serializer.validated_data['password'])
            trainer = Trainer(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                phone_number=serializer.validated_data['phone_number'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                password=password
            )
            trainer.save()
            return Response({'message': 'Trainer created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def trainer_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            user = Trainer.objects.get(username=username)
        except Trainer.DoesNotExist:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if check_password(password, user.password):
            login(request, user)
            return Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)