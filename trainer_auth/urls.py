from django.urls import path
from .views import TrainerDetailView, UpdateTrainerView, TrainerTraineesView


urlpatterns = [
    path("info/", TrainerDetailView.as_view(), name="trainer_info"),
    path("update/", UpdateTrainerView.as_view(), name="update_trainee"),
    path('my-trainees/', TrainerTraineesView.as_view(), name='trainer-trainees'),
]
