from rest_framework import serializers

from sNeeds.apps.store.serializers import SoldTimeSlotSaleSerializer
from ..consultants.models import ConsultantProfile

from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    sold_time_slot_url = serializers.HyperlinkedRelatedField(
        source='sold_time_slot', view_name="store:sold-time-slot-sale-detail",
        lookup_field='id', read_only=True,
    )

    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    url = serializers.HyperlinkedIdentityField(
        view_name="videochat:room-detail", lookup_field='id'
    )

    login_url = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'id', 'url', 'sold_time_slot', 'sold_time_slot_url', 'login_url', 'start_time', 'end_time'
        ]

    def get_login_url(self, obj):
        request = self.context.get("request")
        user = request.user

        if ConsultantProfile.objects.filter(user=user).exists():
            return obj.consultant_login_url
        else:
            return obj.user_login_url

    def get_start_time(self, obj):
        return obj.sold_time_slot.start_time

    def get_end_time(self, obj):
        return obj.sold_time_slot.end_time
