from django.urls import path
from .views import TestCreateView, TestListView, TrainerPupilTestsView, LastTestCheckView

urlpatterns = [
    path('submit/', TestCreateView.as_view(), name='submit-test'),  # POST request
    path('my-tests/', TestListView.as_view(), name='list-tests'),  # GET request
    path('pupil-tests/', TrainerPupilTestsView.as_view(), name='trainer-pupil-tests'),  # GET request
    path('last-test-check/', LastTestCheckView.as_view(), name='last-test-check'),  # GET request
]
