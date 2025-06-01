import pytest
import json
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.urls import path
from rest_framework_simplejwt.tokens import AccessToken
from chat.consumers import ChatConsumer
from mentorship.models import Mentorship
from authentication.models import User
from mentorship.models import Trainer, Trainee

application = URLRouter([
    path("ws/chat/<int:mentorship_id>/", ChatConsumer.as_asgi()),
])

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chat_consumer_message_flow():
    from asgiref.sync import sync_to_async

    # Create users
    trainer_user = await sync_to_async(User.objects.create_user)(
        username="trainer", password="pass", email='abc@gmail.com'
    )
    trainee_user = await sync_to_async(User.objects.create_user)(
        username="trainee", password="pass", email='xyz@gmail.com'
    )

    # Create trainer and trainee profiles
    trainer = await sync_to_async(Trainer.objects.create)(user=trainer_user)
    trainee = await sync_to_async(Trainee.objects.create)(user=trainee_user)

    # Create mentorship linking trainer and trainee
    mentorship = await sync_to_async(Mentorship.objects.create)(
        trainer=trainer, trainee=trainee, is_active=True
    )

    # Generate tokens
    trainee_token = str(AccessToken.for_user(trainee_user))
    trainer_token = str(AccessToken.for_user(trainer_user))

    # --- Test: connection with invalid token ---
    communicator = WebsocketCommunicator(
        application,
        f"/ws/chat/{mentorship.id}/?token=invalidtoken"
    )
    connected, _ = await communicator.connect()
    assert not connected  # Should reject invalid token
    await communicator.disconnect()

    # --- Test: connection without token ---
    communicator = WebsocketCommunicator(
        application,
        f"/ws/chat/{mentorship.id}/"
    )
    connected, _ = await communicator.connect()
    assert not connected  # Should reject missing token
    await communicator.disconnect()

    # --- Test: trainee connects and sends a message ---
    trainee_communicator = WebsocketCommunicator(
        application,
        f"/ws/chat/{mentorship.id}/?token={trainee_token}"
    )
    connected, _ = await trainee_communicator.connect()
    assert connected

    # --- Test: trainer connects separately ---
    trainer_communicator = WebsocketCommunicator(
        application,
        f"/ws/chat/{mentorship.id}/?token={trainer_token}"
    )
    connected, _ = await trainer_communicator.connect()
    assert connected

    # Trainee sends a message
    await trainee_communicator.send_json_to({
        "message": "Hello, trainer!"
    })

    # Trainer should receive the message
    response_from_trainer = await trainer_communicator.receive_json_from()
    assert response_from_trainer["message"] == "Hello, trainer!"
    assert response_from_trainer["sender"] == trainee_user.id
    assert response_from_trainer["receiver"] == trainer_user.id
    assert "timestamp" in response_from_trainer

    # Trainee should also receive the message echo (if your consumer echoes back)
    response_from_trainee = await trainee_communicator.receive_json_from()
    assert response_from_trainee["message"] == "Hello, trainer!"
    assert response_from_trainee["sender"] == trainee_user.id
    assert response_from_trainee["receiver"] == trainer_user.id
    assert "timestamp" in response_from_trainee

    # Trainer sends a reply
    await trainer_communicator.send_json_to({
        "message": "Hello, trainee!"
    })

    # Trainee receives the reply
    response_from_trainee = await trainee_communicator.receive_json_from()
    assert response_from_trainee["message"] == "Hello, trainee!"
    assert response_from_trainee["sender"] == trainer_user.id
    assert response_from_trainee["receiver"] == trainee_user.id
    assert "timestamp" in response_from_trainee

    # Trainer receives own message back if your consumer echoes
    response_from_trainer = await trainer_communicator.receive_json_from()
    assert response_from_trainer["message"] == "Hello, trainee!"
    assert response_from_trainer["sender"] == trainer_user.id
    assert response_from_trainer["receiver"] == trainee_user.id
    assert "timestamp" in response_from_trainer

    # Send multiple messages to test order
    messages = ["msg1", "msg2", "msg3"]
    for msg in messages:
        await trainee_communicator.send_json_to({"message": msg})

        # Trainer should get these messages
        resp = await trainer_communicator.receive_json_from()
        assert resp["message"] == msg

    # Close connections cleanly
    await trainee_communicator.disconnect()
    await trainer_communicator.disconnect()
