from rest_framework import permissions


class IsConsultantPermission(permissions.BasePermission):
    message = 'User should be consultant.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        else:
            if request.user.is_authenticated and request.user.is_consultant():
                return True
            return False