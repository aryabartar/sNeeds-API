from rest_framework import serializers

from sNeeds.apps.store.serializers import SoldTimeSlotSaleSerializer
from sNeeds.apps.account.models import ConsultantProfile

from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    sold_time_slot_url = serializers.HyperlinkedRelatedField(
        source='sold_time_slot', view_name="store:sold-time-slot-sale-detail",
        lookup_field='id', read_only=True,
    )

    login_url = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'id', 'sold_time_slot', 'sold_time_slot_url', 'login_url', 'created'
        ]

    def get_login_url(self, obj):
        request = self.context.get("request")
        user = request.user

        if ConsultantProfile.objects.filter(user=user).exists():
            return obj.consultant_login_url
        else:
            return obj.user_login_url
