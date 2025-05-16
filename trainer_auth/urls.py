from django.urls import path
from .views import (
    TrainerDetailView,
    UpdateTrainerView,
    TrainerTraineesView,
    FilteredTrainerListView,
    CommentCreateView,
    CommentListView,
    CommentDetailView,
    GetTrainerIdByUsername,
    GetTrainerUsernameById,
    TrainerPublicProfileView
)

urlpatterns = [
    path("info/", TrainerDetailView.as_view(), name="trainer_info"),
    path("update/", UpdateTrainerView.as_view(), name="update_trainer"),
    path("my-trainees/", TrainerTraineesView.as_view(), name="trainer_trainees"),
    path("trainers/filter/", FilteredTrainerListView.as_view(), name="filtered_trainer_list"),
    path("comments/create/", CommentCreateView.as_view(), name="comment_create"),
    path("comments/<int:trainer_id>/", CommentListView.as_view(), name="comment_list"),
    path("comments/detail/<int:pk>/", CommentDetailView.as_view(), name="comment_detail"),
    path('trainer-id/<str:username>/', GetTrainerIdByUsername.as_view(), name='get-trainer-id-by-username'),
    path('trainer-username/<int:trainer_id>/', GetTrainerUsernameById.as_view(), name='get-trainer-username-by-id'),
    path('trainers/<int:trainer_id>/profile/', TrainerPublicProfileView.as_view(), name='trainer-public-profile'),

]
