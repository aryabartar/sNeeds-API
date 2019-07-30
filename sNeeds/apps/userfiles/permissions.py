from rest_framework import permissions


class UserFileOwnerPermission(permissions.BasePermission):
    message = "This user is not file owner."

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False
