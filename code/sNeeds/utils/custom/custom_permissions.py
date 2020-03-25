from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsConsultantPermission(permissions.BasePermission):
    message = 'User should be consultant.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        else:
            if request.user.is_authenticated and request.user.is_consultant():
                return True
            return False


class CustomIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if request.method == "OPTIONS":
            return True
        return bool(request.user and request.user.is_authenticated)