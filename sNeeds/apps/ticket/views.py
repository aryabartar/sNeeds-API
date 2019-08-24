from django.db.models import Q

from rest_framework import status, generics, mixins, permissions

from .models import TicketMessage, Ticket
from .serializers import TicketSerializer, MessageSerializer

from .permissions import TicketOwnerPermission, TicketMessageOwnerPermission

from django_filters.rest_framework import DjangoFilterBackend


class TicketListView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        qs = Ticket.objects.filter(
            Q(consultant__user=user) | Q(user=user)
        )

        return qs


class TicketDetailView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [TicketOwnerPermission, permissions.IsAuthenticated]
    lookup_field = 'id'


class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [TicketMessageOwnerPermission, permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['ticket']

    def get_queryset(self):
        user = self.request.user

        qs = TicketMessage.objects.filter(
            Q(ticket__user=user) | Q(ticket__consultant__user=user)
        )

        return qs


class MessageDetailView(generics.RetrieveAPIView):
    queryset = TicketMessage.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [TicketMessageOwnerPermission, permissions.IsAuthenticated]
    lookup_field = 'id'
