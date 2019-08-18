from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework import status, generics, mixins, permissions

from sNeeds.apps.account.models import ConsultantProfile
from sNeeds.apps.customAuth.models import CustomUser

from .models import TicketMessage
from .serializers import TicketSerializer

from .permissions import TicketOwnerPermission


class TweetListAPIView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [TicketOwnerPermission, permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        qs = TicketMessage.objects.filter(
            Q(ticket__consultant_id=user.id) | Q(ticket__user_id=user.id)
        )

        return qs


class ListTicket(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [TicketOwnerPermission, permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        ticket_id = self.kwargs['id']

        qs = TicketMessage.objects.filter(
            Q(ticket__consultant_id=user.id) | Q(ticket__user_id=user.id) | Q(ticket_id=ticket_id)
        )

        return qs


class TweetDetailAPIView(generics.RetrieveAPIView):
    queryset = TicketMessage.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [TicketOwnerPermission, permissions.IsAuthenticated]
    lookup_field = 'pk'
