from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_datetime
from .models import Message
from .serializers import MessageSerializer
from mentorship.models import Mentorship

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start', openapi.IN_QUERY, description="Start datetime (ISO 8601)", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'end', openapi.IN_QUERY, description="End datetime (ISO 8601)", type=openapi.TYPE_STRING, required=True
            ),
        ],
        responses={200: MessageSerializer(many=True)},
        operation_description="Retrieve chat history between the authenticated user and their mentorship partner within the given time interval."
    )
    def get(self, request, mentorship_id):
        start = request.query_params.get('start')
        end = request.query_params.get('end')

        try:
            mentorship = Mentorship.objects.get(id=mentorship_id, is_active=True)
        except Mentorship.DoesNotExist:
            return Response({"detail": "Mentorship not found."}, status=404)

        if request.user not in [mentorship.trainee.user, mentorship.trainer.user]:
            return Response({"detail": "Unauthorized."}, status=403)

        messages = Message.objects.filter(
            mentorship=mentorship,
            timestamp__range=(parse_datetime(start), parse_datetime(end))
        ).order_by('timestamp')

        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data)
