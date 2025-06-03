from django.utils import timezone
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from jwt import decode as jwt_decode
from django.conf import settings
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser
from authentication.models import User
from .models import Message
from mentorship.models import Mentorship

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope)
        self.mentorship_id = self.scope['url_route']['kwargs']['mentorship_id']
        self.room_group_name = f'mentorship_{self.mentorship_id}'

        # Parse token from query string
        token = self.scope['query_string'].decode().split('=')[-1]
        try:
            UntypedToken(token)
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = await get_user(decoded_data["user_id"])
            self.scope['user'] = user
        except (InvalidToken, TokenError, KeyError):
            await self.close()
            return

        self.mentorship = await self.get_mentorship(self.mentorship_id)
        # print("from try:",decoded_data)
        # print(self.mentorship)
        # if not self.mentorship or not self.scope["user"].is_authenticated:
        #     await self.close()
        #     return

        # Check if user is part of the mentorship
        print(self.mentorship_id)
        is_participant = await self.is_user_in_mentorship(self.mentorship, self.scope["user"])
        if not is_participant:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.mark_messages_as_seen(self.scope["user"])


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope["user"]

        if data.get("type") == "mark_seen":
            await self.mark_messages_as_seen(self.scope["user"])
            return
        # Infer receiver based on mentorship
        receiver = (
            self.mentorship.trainer.user if sender == self.mentorship.trainee.user
            else self.mentorship.trainee.user
        )

        saved = await self.save_message(sender.id, receiver.id, message)

        await self.mark_messages_as_seen(sender)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': saved['content'],
                'sender': saved['sender_id'],
                'receiver': saved['receiver_id'],
                'timestamp': saved['timestamp'],
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, content):
        message = Message.objects.create(
            mentorship=self.mentorship,
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
        )
        return {
            'content': message.content,
            'sender_id': message.sender_id,
            'receiver_id': message.receiver_id,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

    @database_sync_to_async
    def get_mentorship(self, mentorship_id):
        try:
            return Mentorship.objects.get(id=mentorship_id, is_active=True)
        except Mentorship.DoesNotExist:
            return None
    @database_sync_to_async
    def is_user_in_mentorship(self, mentorship, user):
        return user in [mentorship.trainee.user, mentorship.trainer.user]
    @database_sync_to_async
    def mark_messages_as_seen(self, user):
        Message.objects.filter(
            mentorship=self.mentorship,
            receiver=user,
            seen=False
        ).update(seen=True, seen_at=timezone.now())
