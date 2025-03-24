from django.urls import path
from .views import SubmitTestView

urlpatterns = [
    path('submit/', SubmitTestView.as_view(), name='submit-test'),
]
