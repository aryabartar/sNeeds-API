from django.db.models import Q

from rest_framework import permissions

from sNeeds.apps.ticket.models import Ticket, TicketMessage


class TicketOwnerPermission(permissions.BasePermission):
    message = "You are not owner of this ticket."

    def has_permission(self, request, view):
        user = request.user

        if request.user.is_anonymous:
            return False

        ticket_id = view.kwargs.get('id', None)

        try:
            Ticket.objects.filter(
                Q(pk=ticket_id) & (Q(user=user) | Q(consultant__user=user))
            )
        except Ticket.DoesNotExist:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if obj.user == user or obj.consultant.user == user:
            return True

        return False


class TicketMessageOwnerPermission(permissions.BasePermission):
    message = "You are not owner of this Message."

    def has_permission(self, request, view):
        user = request.user

        try:
            TicketMessage.objects.filter(
                Q(ticket__consultant__user=user) | Q(ticket__user=user)
            )
        except Ticket.DoesNotExist:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if obj.ticket.user == user or obj.ticket.consultant == user:
            return True

        return False