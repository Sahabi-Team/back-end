import pytest
from rest_framework.test import APIClient
from exercise.models import Exercise, ExerciseTag, MuscleGroup, Equipment

@pytest.mark.django_db
def test_exercise_list_view():
    Exercise.objects.create(name="Push Up", description="A classic exercise.", difficulty="مبتدی", workoutplaces="خانه")
    client = APIClient()
    response = client.get('/api/exercises/')
    assert response.status_code == 200
    assert response.data[0]['name'] == "Push Up"

@pytest.mark.django_db
def test_filtered_exercise_list_view_by_tag():
    tag = ExerciseTag.objects.create(name="Strength")
    ex = Exercise.objects.create(name="Squat", description="Legs workout", difficulty="متوسط", workoutplaces="باشگاه")
    ex.tags.add(tag)

    client = APIClient()
    response = client.get('/api/exercises/filter/', {'tags': 'Strength'})
    assert response.status_code == 200
    assert response.data[0]['name'] == "Squat"

@pytest.mark.django_db
def test_filtered_exercise_list_view_by_difficulty():
    Exercise.objects.create(name="Sit Up", description="Abs workout", difficulty="پیشرفته", workoutplaces="خانه")

    client = APIClient()
    response = client.get('/api/exercises/filter/', {'difficulty': 'پیشرفته'})
    assert response.status_code == 200
    assert response.data[0]['name'] == "Sit Up"

@pytest.mark.django_db
def test_filtered_exercise_list_view_search():
    Exercise.objects.create(name="Pull Up", description="Back workout", difficulty="متوسط", workoutplaces="خانه")

    client = APIClient()
    response = client.get('/api/exercises/filter/', {'search': 'Pull'})
    assert response.status_code == 200
    assert response.data[0]['name'] == "Pull Up"

