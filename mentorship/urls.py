from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MentorshipViewSet

router = DefaultRouter()
router.register(r'mentorships', MentorshipViewSet, basename='mentorship')

urlpatterns = [
    path('', include(router.urls)),
] 