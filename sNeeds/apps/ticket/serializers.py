from rest_framework import serializers
from .models import TicketMessage

from sNeeds.apps.customAuth.serializers import SafeUserDataSerializer


class TicketSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="ticket:ticketMessages-detail", lookup_field='id'
    )
    user = serializers.SerializerMethodField()
    consultant = serializers.SerializerMethodField()

    class Meta:
        model = TicketMessage
        fields = [
            'id',
            'url',
            'ticket',
            'user',
            'consultant',
            'file',
            'text',
        ]

    def get_user(self, obj):
        request = self.context.get("request")
        return SafeUserDataSerializer(
            obj.ticket.user, context={"request": request}
        ).data

    def get_consultant(self, obj):
        request = self.context.get("request")
        return SafeUserDataSerializer(
            obj.ticket.consultant, context={"request": request}
        ).data
