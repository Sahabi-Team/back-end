from django.urls import path
from .views import TrainerDetailView, UpdateTrainerView


urlpatterns = [
    path("info/", TrainerDetailView.as_view(), name="trainee_info"),
    path("update/", UpdateTrainerView.as_view(), name="update_trainee"),
]
