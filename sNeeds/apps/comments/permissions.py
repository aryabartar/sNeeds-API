from rest_framework import permissions


class CommentOwnerPermission(permissions.BasePermission):
    message = "This user is not comment owner."

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False


class SoldTimeSlotRateOwnerPermission(permissions.BasePermission):
    message = "This user is not rate owner."

    def has_object_permission(self, request, view, obj):
        if request.user == obj.sold_time_slot.sold_to:
            return True

        return False
