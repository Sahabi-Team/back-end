from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'workout-plans', views.WorkoutPlanViewSet, basename='workout-plan')
router.register(r'workout-exercises', views.WorkoutExerciseViewSet, basename='workout-exercise')

urlpatterns = [
    path('', include(router.urls)),
]
