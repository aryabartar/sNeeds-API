from rest_framework import permissions


class CartOwnerPermission(permissions.BasePermission):
    message = "This user is not cart owner."

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False



