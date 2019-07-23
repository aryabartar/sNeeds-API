from rest_framework import permissions


class CommentOwnerPermission(permissions.BasePermission):
    message = "This user is not comment owner."

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False
