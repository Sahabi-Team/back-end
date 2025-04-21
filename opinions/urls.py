from django.urls import path
from .views import OpinionListView, OpinionCreateUpdateView

urlpatterns = [
    path('', OpinionListView.as_view(), name='opinion-list'),
    path('my/', OpinionCreateUpdateView.as_view(), name='opinion-create-update'),
]
