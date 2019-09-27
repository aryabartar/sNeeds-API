from rest_framework import permissions


class ChatOwnerPermission(permissions.BasePermission):
    message = "This user is not in the chat."

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user == obj.user or user == obj.consultant.user:
            return True
        return False
