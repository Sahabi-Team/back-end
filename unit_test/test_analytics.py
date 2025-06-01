import pytest
from rest_framework.test import APIClient
from trainer_auth.models import Trainer
from client_auth.models import Trainee
from exercise.models import Exercise
from workout.models import WorkoutPlan
from django.contrib.auth.hashers import make_password
from trainer_auth.models import Trainer
from client_auth.models import Trainee
from authentication.models import User

pytestmark = pytest.mark.django_db

client = APIClient()



def test_total_clients_view(client):
    # Create user with usertype trainee
    user1 = User.objects.create(
        username="trainee1",
        password=make_password("pass123"),
        email="t1@example.com",
        usertype=User.TRAINEE
    )
    Trainee.objects.create(user=user1)
    
    user2 = User.objects.create(
        username="trainee2",
        password=make_password("pass123"),
        email="t2@example.com",
        usertype=User.TRAINEE
    )
    Trainee.objects.create(user=user2)

    response = client.get('/api/analytics/total-clients/')
    assert response.status_code == 200
    assert response.data == {"total_clients": 2}


def test_total_trainers_view(client):
    user = User.objects.create(
        username="trainer1",
        password=make_password("pass123"),
        email="tr1@example.com",
        usertype=User.TRAINER
    )
    Trainer.objects.create(user=user)

    response = client.get('/api/analytics/total-trainers/')
    assert response.status_code == 200
    assert response.data == {"total_trainers": 1}

def test_total_workout_plans_view():
    WorkoutPlan.objects.create(name="Plan A", description="desc")
    WorkoutPlan.objects.create(name="Plan B", description="desc")

    response = client.get('/api/analytics/total-workout-plans/')
    assert response.status_code == 200
    assert response.data == {"total_workout_plans": 2}


def test_total_exercises_view():
    Exercise.objects.create(name="Push-up", description="Chest")
    Exercise.objects.create(name="Squat", description="Legs")

    response = client.get('/api/analytics/total-exercises/')
    assert response.status_code == 200
    assert response.data == {"total_exercises": 2}
