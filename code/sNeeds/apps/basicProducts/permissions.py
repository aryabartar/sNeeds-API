from rest_framework.permissions import BasePermission


class SoldBasicProductOwnerPermission(BasePermission):
    message = "User must be basic product purchaser."

    def has_object_permission(self, request, view, obj):
        user = request.user

        if obj.sold_to == user:
            return True

        return False
