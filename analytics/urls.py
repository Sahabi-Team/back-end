# analytics/urls.py
from django.urls import path
from .views import (
    TotalClientsView,
    TotalTrainersView,
    TotalWorkoutPlansView,
    TotalExercisesView,
)

urlpatterns = [
    path('total-clients/', TotalClientsView.as_view(), name='total-clients'),
    path('total-trainers/', TotalTrainersView.as_view(), name='total-trainers'),
    path('total-workout-plans/', TotalWorkoutPlansView.as_view(), name='total-workout-plans'),
    path('total-exercises/', TotalExercisesView.as_view(), name='total-exercises'),
]
