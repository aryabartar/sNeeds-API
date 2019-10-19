from django.db.models import Q

from rest_framework import status, generics, mixins, permissions
from rest_framework import filters
from django_filters import rest_framework as custom_filters

from .models import Message, Ticket
from .serializers import TicketSerializer, MessageSerializer, TicketConsultantsSerializer

from .permissions import TicketOwnerPermission, MessageOwnerPermission
from .filtersets import MessageFilter

from sNeeds.apps.store.models import SoldTimeSlotSale


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
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, custom_filters.DjangoFilterBackend, ]
    filterset_class = MessageFilter
    ordering_fields = ['created']

    def get_queryset(self):
        user = self.request.user

        qs = Message.objects.filter(
            Q(ticket__user=user) | Q(ticket__consultant__user=user)
        )

        return qs


class MessageDetailView(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [MessageOwnerPermission, permissions.IsAuthenticated]
    lookup_field = 'id'


class TicketConsultantsView(generics.ListAPIView):
    serializer_class = TicketConsultantsSerializer

    def get_queryset(self):
        user = self.request.user
        return SoldTimeSlotSale.objects.filter(sold_to=user).order_by('consultant').distinct('consultant')