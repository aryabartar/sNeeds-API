from rest_framework import permissions


class TweetOwnerPermission(permissions.BasePermission):
    message = "This user is not tweet owner."

    def has_object_permission(self, request, view, obj):
        user = request.user

        if obj.sender == user or obj.receiver == user:
            return True

        return False
