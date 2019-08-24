from rest_framework import serializers
from rest_framework.reverse import reverse


from sNeeds.apps.account.serializers import ConsultantProfileSerializer
from sNeeds.apps.account.models import ConsultantProfile


class ConsultantSerializer(serializers.Field):
    def to_representation(self, value):
        return ConsultantProfileSerializer(value, context={'request': self.context['request']}).data

    def to_internal_value(self, id):
        try:
            id = int(id)
        except ValueError:
           raise serializers.ValidationError("Provide id of consultant in numbers, please.")
        try:
            consultant = ConsultantProfile.objects.get(pk=id)
        except ConsultantProfile.DoesNotExist:
            raise serializers.ValidationError("Such a consultant does not exist")
        return consultant


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