from django.db.models import Q

from rest_framework import permissions

from sNeeds.apps.ticket.models import Ticket, Message


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
        ticket_id = view.kwargs.get('id')

        if obj.id == ticket_id and (obj.user == user or obj.consultant.user == user):
            return True

        return False


class MessageOwnerPermission(permissions.BasePermission):
    message = "You are not owner of this Message."

    def has_permission(self, request, view):
        user = request.user
        message_id = view.kwargs.get('id')

        try:
            Message.objects.filter(
                Q(pk=message_id) & (Q(ticket__consultant__user=user) | Q(ticket__user=user))
            )
        except Ticket.DoesNotExist:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        message_id = view.kwargs.get('id')

        if obj.id == message_id and (obj.ticket.user == user or obj.ticket.consultant.user == user):
            return True

        return False
