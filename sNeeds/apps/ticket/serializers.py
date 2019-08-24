from rest_framework import serializers
from .models import TicketMessage

from .models import Ticket
from .custom_serializer import ConsultantSerializer, TicketUrlSerializer, TicketMessageUrlSerializer

from sNeeds.apps.customAuth.serializers import SafeUserDataSerializer
from sNeeds.apps.account.serializers import ConsultantProfileSerializer


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    consultant = ConsultantSerializer()
    brief_detail_url = TicketUrlSerializer(
        view_name="ticket:ticket_brief-detail"
    )
    comprehensive_detail_url = TicketUrlSerializer(
        view_name="ticket:ticket_comprehensive-detail"
    )

    class Meta:
        model = Ticket
        fields = [
            'id',
            'brief_detail_url',
            'comprehensive_detail_url',
            'title',
            'user',
            'consultant',
            'created',
        ]

        extra_kwargs = {
            'user': {'read_only': True},
            'created': {'read_only': True},
            'brief_detail_url': {'read_only': True},
            'comprehensive_detail_url': {'read_only': True},
        }

    def get_user(self, obj):
        request = self.context.get("request")
        return SafeUserDataSerializer(
            obj.user, context={"request": request}
        ).data

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        obj = Ticket.objects.create(
            title=validated_data.get('title'),
            user=user,
            consultant=validated_data.get('consultant'),
        )

        return obj


class TicketMessageSerializer(serializers.ModelSerializer):
    url = TicketMessageUrlSerializer(
        view_name="ticket:ticketMessages-detail"
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
        return ConsultantProfileSerializer(
            obj.ticket.consultant, context={"request": request}
        ).data
