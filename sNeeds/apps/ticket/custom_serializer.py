from django.db.models import Q

from rest_framework import serializers
from rest_framework.reverse import reverse

from sNeeds.apps.account.serializers import SafeConsultantProfileSerializer
from sNeeds.apps.account.models import ConsultantProfile


class ConsultantFieldSerializer(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        tmp = super(ConsultantFieldSerializer, self).to_representation(value)
        sal = ConsultantProfile.objects.get(pk=tmp)
        return str(SafeConsultantProfileSerializer(
            sal, context={"request": self.context['request']}
        ).data)


class TicketUrlSerializer(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'ticket_id': obj.id,
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)


class TicketMessageUrlSerializer(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'ticket_id': obj.ticket.id,
            'ticket_message_id': obj.id
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)


class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(UserFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(
           Q(user= request.user) | Q(consultant__user=request.user)
        )