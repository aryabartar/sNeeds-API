from rest_framework import permissions

from sNeeds.apps.ticket.models import Ticket


class TicketOwnerPermission(permissions.BasePermission):
    message = "..."

    def has_permission(self, request, view):
        user = request.user
        id = view.kwargs.get('id', None)

        if id is None:
            return False

        try:
            Ticket.objects.get(id=id, user=user)

        except Ticket.DoesNotExist:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if obj.ticket.user == user or obj.ticket.consultant == user:
            return True

        return False

# class TicketOwnerPermission(permissions.BasePermission):
#     message = "This user is not ticket owner."
#
#     def has_object_permission(self, request, view, obj):
#         user = request.user
#
#         if obj.user == user or obj.consultant == user:
#             return True
#
#         return False
