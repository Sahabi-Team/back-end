import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import timedelta
from mentorship.models import Mentorship, Trainer, Trainee
from chat.models import Message
from authentication.models import User


@pytest.mark.django_db
def test_chat_history_view_returns_messages_within_range():
    client = APIClient()

    # Create users
    user1 = User.objects.create_user(email="trainer100@gmail.com",username='trainer100', password='trainer100', usertype='trainer')
    user2 = User.objects.create_user(email="trainee100@gmail.com",username='trainee100', password='trainee100', usertype='trainee')

    # Create trainer and trainee
    trainer = Trainer.objects.create(user=user1)
    trainee = Trainee.objects.create(user=user2)

    # Create mentorship
    mentorship = Mentorship.objects.create(trainer=trainer, trainee=trainee, is_active=True)

    # Create messages
    now = timezone.now()
    msg1_time = now - timedelta(hours=2)
    msg2_time = now - timedelta(hours=1)
    msg1 = Message.objects.create(
        mentorship=mentorship,
        sender=user1,
        receiver=user2,
        content="Hello!",
        timestamp=msg1_time
    )

    msg2 = Message.objects.create(
        mentorship=mentorship,
        sender=user2,
        receiver=user1,
        content="Hi!",
        timestamp=msg2_time
    )

    Message.objects.create(
        mentorship=mentorship,
        sender=user1,
        receiver=user2,
        content="Too late",
        timestamp=now + timedelta(hours=2)  # should be excluded
    )
    # Authenticate as trainer
    client.force_authenticate(user=user1)

    # Call API
    url = reverse('chat-history', args=[mentorship.id])
    response = client.get(url, {
        'start': (now - timedelta(hours=3)).isoformat(),
        'end': (now + timedelta(minutes=30)).isoformat()
    })

    # Assertions
    assert response.status_code == 200
    data = response.json()
    print(data)
    # Sort by timestamp just in case of instability
    contents = [msg['text'] for msg in sorted(data, key=lambda m: m['time'])]
    assert len(contents) == 2
    assert "Hello!" in contents
    assert "Hi!" in contents
    assert "Too late" not in contents
