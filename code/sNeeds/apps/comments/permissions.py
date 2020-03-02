from rest_framework import permissions


class SoldTimeSlotRateOwnerPermission(permissions.BasePermission):
    message = "This user is not rate owner."

    def has_object_permission(self, request, view, obj):
        print('hey')
        if request.user == obj.sold_time_slot.sold_to:
            return True

        return False

    def has_permission(self, request, view):
        print("no")
        return True