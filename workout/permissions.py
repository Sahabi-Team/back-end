from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from mentorship.models import Mentorship

class IsTrainerOfMentorship(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_trainer

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if not request.user.is_trainer:
            return False
        mentorship = Mentorship.objects.get(id=obj.mentorship.id)
        return mentorship.trainer == request.user 