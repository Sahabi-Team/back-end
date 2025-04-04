from django.urls import path
from .views import ExerciseListView, FilteredExerciseListView

urlpatterns = [
    path('', ExerciseListView.as_view(), name='exercise-list'),
    path('filter/', FilteredExerciseListView.as_view(), name='filtered-exercise-list'),
]
