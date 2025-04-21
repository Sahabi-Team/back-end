# urls.py
from django.urls import path
from .views import TraineeWorkoutPlansView

urlpatterns = [
    path('trainee/workout-plans/', TraineeWorkoutPlansView.as_view(), name='trainee-workout-plans'),
]
