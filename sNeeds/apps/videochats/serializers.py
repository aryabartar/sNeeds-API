from rest_framework import serializers

from sNeeds.apps.store.serializers import SoldTimeSlotSaleSerializer

from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    sold_time_slot_url = serializers.HyperlinkedRelatedField(
        source='sold_time_slot', view_name="store:time-slot-sale-detail",
        lookup_field='id', read_only=True,
    )

    class Meta:
        model = Room
        fields = [
            'id', 'sold_time_slot', 'sold_time_slot_url', 'user_login_url', 'consultant_login_url', 'created'
        ]
