from django.db.models import Q

from rest_framework import status, generics, mixins, permissions

from .models import TicketMessage, Ticket
from .serializers import TicketSerializer, TicketMessageSerializer

from .permissions import TicketOwnerPermission


class TicketListView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        qs = Ticket.objects.filter(
            Q(consultant_id=user.id) | Q(user_id=user.id)
        )

        return qs


class TicketDetailView(generics.RetrieveAPIView): #  TODO:permissions are not working!!!!
    serializer_class = TicketSerializer
    permissions_classes = [permissions.IsAuthenticated, TicketOwnerPermission]
    queryset = Ticket.objects.all()

    def get_object(self):
        ticket_id = self.kwargs['ticket_id']
        ticket = Ticket.objects.get(id=ticket_id)
        return ticket


class TicketMessagesListView(generics.ListCreateAPIView):
    serializer_class = TicketMessageSerializer
    permission_classes = [TicketOwnerPermission, permissions.IsAuthenticated]

    def get_queryset(self):
        ticket_id = self.kwargs['ticket_id']

        qs = TicketMessage.objects.filter(
            Q(ticket_id=ticket_id)
        )

        return qs


class TicketMessageDetailView(generics.RetrieveAPIView):
    queryset = TicketMessage.objects.all()
    serializer_class = TicketMessageSerializer
    permission_classes = [TicketOwnerPermission, permissions.IsAuthenticated]

    def get_object(self):
        ticket_id = self.kwargs['ticket_id']
        ticket_message_id = self.kwargs['ticket_message_id']
        ticket_message = TicketMessage.objects.get(id=ticket_message_id, ticket_id=ticket_id)
        return ticket_message
