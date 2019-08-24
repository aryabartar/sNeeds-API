from rest_framework import permissions

from sNeeds.apps.ticket.models import Ticket


class TicketOwnerPermission(permissions.BasePermission):
    message = "..."

    def has_permission(self, request, view):
        user = request.user

        ticket_id = view.kwargs.get('ticket_id', None)

        if ticket_id is None:
            return False

        if request.user.is_anonymous:
            return False

        try:
            Ticket.objects.get(id=ticket_id, user=user)
        except Ticket.DoesNotExist:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.user.is_anonymous:
            return False

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
