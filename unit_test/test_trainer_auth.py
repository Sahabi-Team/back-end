import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from authentication.models import User
from trainer_auth.models import Trainer  # adjust path if needed

@pytest.mark.django_db
def test_trainer_detail_view_authenticated_success():
    client = APIClient()

    # Create user and trainer profile
    user = User.objects.create_user(username='trainer_test', password='test123', usertype='trainer')
    trainer = Trainer.objects.create(user=user, bio="Fitness expert", experience=5, price=100.0)

    # Authenticate
    client.force_authenticate(user=user)

    url = reverse('trainer_info')
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    print(data);
    assert data['user']['id'] == user.id
    assert data['bio'] == "Fitness expert"
    assert data['experience'] == 5
    assert data['price'] == 100.0

@pytest.mark.django_db
def test_trainer_detail_view_unauthenticated():
    client = APIClient()
    url = reverse('trainer_info')
    response = client.get(url)

    assert response.status_code == 401  # Unauthorized

@pytest.mark.django_db
def test_trainer_detail_view_no_trainer_profile():
    client = APIClient()

    # Create user with no trainer profile
    user = User.objects.create_user(username='no_profile', password='test123', usertype='trainer')
    client.force_authenticate(user=user)

    url = reverse('trainer_info')
    response = client.get(url)
    assert response.status_code == 404
    assert response.json()['message'] == "Trainer profile not found"


import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from authentication.models import User
from trainer_auth.models import Trainer
from django.db.models import Avg

@pytest.mark.django_db
def test_filtered_trainer_list_view():
    client = APIClient()

    # Create users and trainers
    user1 = User.objects.create_user(username='user1', email='user1@example.com', password='pass')
    user2 = User.objects.create_user(username='user2', email='user2@example.com', password='pass')
    user3 = User.objects.create_user(username='john_doe', email='john@example.com', password='pass')

    Trainer.objects.create(
        user=user1,
        bio='Bio1',
        experience=5,
        isAvailableForReservation=True,
        price=100.0,
        specialties='yoga'
    )
    Trainer.objects.create(
        user=user2,
        bio='Bio2',
        experience=8,
        isAvailableForReservation=False,
        price=150.0,
        specialties='crossfit'
    )
    Trainer.objects.create(
        user=user3,
        bio='Bio3',
        experience=3,
        isAvailableForReservation=True,
        price=120.0,
        specialties='yoga'
    )

    url = reverse('filtered_trainer_list')

    # Test: no filters - should return all 3
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3

    # Test: search by username
    response = client.get(url, {'search': 'john'})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['user']['username'] == 'john_doe'

    # Test: filter by specialties (yoga)
    response = client.get(url, {'specialties': 'yoga'})
    assert response.status_code == 200
    # Both user1 and user3 have yoga
    assert len(response.data) == 2

    # Test: filter by experience range 4-6 (should include user1 only)
    response = client.get(url, {'experience': '4-6'})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['experience'] == 5

    # Test: filter by price_min=110 (should exclude user1)
    response = client.get(url, {'price_min': '110'})
    assert response.status_code == 200
    assert all(t['price'] >= 110 for t in response.data)

    # Test: filter by availability = true (should exclude user2)
    response = client.get(url, {'available': 'true'})
    assert response.status_code == 200
    assert all(t['isAvailableForReservation'] for t in response.data)

    # Test ordering by experience ascending
    response = client.get(url, {'ordering': 'experience'})
    assert response.status_code == 200
    exps = [t['experience'] for t in response.data]
    assert exps == sorted(exps)

    # Test ordering by experience descending
    response = client.get(url, {'ordering': '-experience'})
    assert response.status_code == 200
    exps_desc = [t['experience'] for t in response.data]
    assert exps_desc == sorted(exps_desc, reverse=True)



import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User
from trainer_auth.models import Trainer, Comment
from client_auth.models import Trainee

@pytest.mark.django_db
def test_comment_create_view():
    client = APIClient()

    user = User.objects.create_user(
        username='trainee1', password='pass', email='trainee1@example.com'
    )
    trainee = Trainee.objects.create(user=user)

    trainer_user = User.objects.create_user(
        username='trainer1', password='pass', email='trainer1@example.com'
    )
    trainer = Trainer.objects.create(user=trainer_user, experience=3, price=100)

    client.force_authenticate(user=user)
    url = reverse('comment_create')

    data = {
        'trainer': trainer.id,
        'rating': 4,
        'comment': 'Great trainer!'
    }

    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Comment.objects.filter(trainer=trainer, trainee=trainee).exists()


@pytest.mark.django_db
def test_comment_list_view():
    client = APIClient()

    trainer_user = User.objects.create_user(
        username='trainer2', password='pass', email='trainer2@example.com'
    )
    trainer = Trainer.objects.create(user=trainer_user, experience=5)

    trainee_user = User.objects.create_user(
        username='trainee2', password='pass', email='trainee2@example.com'
    )
    trainee = Trainee.objects.create(user=trainee_user)

    for i in range(3):
        Comment.objects.create(
            trainer=trainer,
            rating=4,
            comment=f'Comment {i}',
            trainee=trainee
        )

    url = reverse('comment_list', kwargs={'trainer_id': trainer.id})

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3


@pytest.mark.django_db
def test_comment_detail_view():
    client = APIClient()

    user = User.objects.create_user(
        username='trainee3', password='pass', email='trainee3@example.com'
    )
    trainee = Trainee.objects.create(user=user)
    trainer_user = User.objects.create_user(
        username='trainer3', password='pass', email='trainer3@example.com'
    )
    trainer = Trainer.objects.create(user=trainer_user)

    comment = Comment.objects.create(
        trainer=trainer,
        rating=5,
        comment='Awesome',
        trainee=trainee
    )

    client.force_authenticate(user=user)
    url = reverse('comment_detail', kwargs={'pk': comment.id})

    # Retrieve
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['comment'] == 'Awesome'

    # Update
    response = client.patch(url, {'comment': 'Updated comment'})
    assert response.status_code == status.HTTP_200_OK
    comment.refresh_from_db()
    assert comment.comment == 'Updated comment'

    # Delete
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Comment.objects.filter(id=comment.id).exists()



@pytest.mark.django_db
def test_get_trainer_id_by_username_view():
    client = APIClient()

    user = User.objects.create_user(username='trainer4', password='pass')
    trainer = Trainer.objects.create(user=user)

    url = reverse('get-trainer-id-by-username', kwargs={'username': 'trainer4'})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['trainer_id'] == trainer.id


@pytest.mark.django_db
def test_get_trainer_username_by_id_view():
    client = APIClient()

    user = User.objects.create_user(username='trainer5', password='pass')
    trainer = Trainer.objects.create(user=user)

    url = reverse('get-trainer-username-by-id', kwargs={'trainer_id': trainer.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == user.username


@pytest.mark.django_db
def test_trainer_public_profile_view():
    client = APIClient()

    user = User.objects.create_user(username='trainer6', password='pass')
    trainer = Trainer.objects.create(user=user)

    url = reverse('trainer-public-profile', kwargs={'trainer_id': trainer.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['user']['username'] == user.username

    # Non-existing trainer_id returns 404
    url = reverse('trainer-public-profile', kwargs={'trainer_id': 9999})
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
