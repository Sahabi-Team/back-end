from django.urls import path
from .views import TestCreateView, TestListView

urlpatterns = [
    path('submit/', TestCreateView.as_view(), name='submit-test'),  # POST request
    path('my-tests/', TestListView.as_view(), name='list-tests'),  # GET request
]
