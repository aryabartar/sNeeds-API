from rest_framework import permissions


class OrderOwnerPermission(permissions.BasePermission):
    message = "This user is not order owner."

    def has_object_permission(self, request, view, obj):
        if request.user == obj.get_user():
            return True
        return False


