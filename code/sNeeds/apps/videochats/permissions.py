from rest_framework import permissions


class RoomOwnerPermission(permissions.BasePermission):
    message = "This user has not room permission."

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user == obj.sold_time_slot.sold_to or \
                user == obj.sold_time_slot.consultant.user:
            return True
        return False
