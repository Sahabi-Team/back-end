from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_datetime

from client_auth.models import Trainee
from trainer_auth.models import Trainer
from .models import Message
from .serializers import MessageSerializer
from mentorship.models import Mentorship

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Count, Max, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
            mentorship = Mentorship.objects.get(id=mentorship_id)
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



class UnreadMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Try getting the user as a trainee or trainer
        try:
            trainee = Trainee.objects.get(user=user)
        except Trainee.DoesNotExist:
            trainee = None

        try:
            trainer = Trainer.objects.get(user=user)
        except Trainer.DoesNotExist:
            trainer = None

        # Get mentorships where the user is either the trainee or trainer
        mentorships = Mentorship.objects.filter(
            Q(trainee=trainee) | Q(trainer=trainer)
        )

        result = []
        for mentorship in mentorships:
            if trainee and mentorship.trainee == trainee:
                other_user = mentorship.trainer.user
            else:
                other_user = mentorship.trainee.user

            unread = Message.objects.filter(
                mentorship=mentorship,
                receiver=user,
                seen=False
            )

            unread_count = unread.count()
            last_message = unread.order_by('-timestamp').first()

            result.append({
                "user_id": other_user.id,
                "mentorship_id":mentorship.id,
                "username": other_user.username,
                "unread_count": unread_count,
                "last_message": last_message.content if last_message else None
            })

        return Response(result)