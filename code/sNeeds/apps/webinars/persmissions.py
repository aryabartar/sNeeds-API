from rest_framework.permissions import BasePermission


class SoldWebinarOwnerPermission(BasePermission):
    message = "This user is not sold webinar owner."

    def has_object_permission(self, request, view, obj):
        user = request.user

        if obj.sold_to == user:
            return True

        return False
