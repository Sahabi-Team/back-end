from rest_framework.permissions import BasePermission

class IsTrainee(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "trainee_profile")

class IsTrainer(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "trainer_profile")
