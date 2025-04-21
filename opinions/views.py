from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .models import Opinion
from .serializers import OpinionSerializer

class OpinionListView(generics.ListAPIView):
    queryset = Opinion.objects.all().order_by('-created_at')
    serializer_class = OpinionSerializer
    permission_classes = [permissions.AllowAny]

class OpinionCreateUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=OpinionSerializer)  
    def post(self, request):

        if Opinion.objects.filter(user=request.user).exists():
            return Response({'detail': 'Opinion already exists. Use PUT to update.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OpinionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=OpinionSerializer) 
    def put(self, request):
        opinion = Opinion.objects.filter(user=request.user).first()
        if not opinion:
            return Response({'detail': 'Opinion not found. Use POST to create.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OpinionSerializer(opinion, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        opinion = Opinion.objects.filter(user=request.user).first()
        if not opinion:
            return Response({'detail': 'No opinion found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OpinionSerializer(opinion)
        return Response(serializer.data)
