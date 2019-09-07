from django.db.models import Q

from .models import Message, Ticket

from django_filters import rest_framework as filters


def get_queryset(request):
    return Ticket.objects.filter(
        Q(user=request.user) | Q(consultant__user=request.user)
    )


class MessageFilter(filters.FilterSet):
    ticket = filters.ModelChoiceFilter(field_name='ticket', queryset=get_queryset)

    class Meta:
        model = Message
        fields = ['ticket']