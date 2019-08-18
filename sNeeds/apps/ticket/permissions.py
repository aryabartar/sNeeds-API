from rest_framework import permissions


class TicketOwnerPermission(permissions.BasePermission):
    message = "This user is not ticket owner."

    def has_object_permission(self, request, view, obj):
        user = request.user

        if obj.ticket.user == user or obj.ticket.consultant == user:
            return True

        return False
