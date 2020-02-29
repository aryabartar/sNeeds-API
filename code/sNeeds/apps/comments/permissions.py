from rest_framework import permissions


class SoldTimeSlotRateOwnerPermission(permissions.BasePermission):
    message = "This user is not rate owner."

    def has_object_permission(self, request, view, obj):
        if request.user == obj.sold_time_slot.sold_to:
            return True

        return False
