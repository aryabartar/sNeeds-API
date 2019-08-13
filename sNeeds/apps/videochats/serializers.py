from rest_framework import serializers

from sNeeds.apps.store.serializers import SoldTimeSlotSaleSerializer

from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    time_slot = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'sold_time_slot', 'consultant_login_url', 'user_login_url']

    def get_time_slot(self, obj):
        return SoldTimeSlotSaleSerializer(obj.sold_time_slot).data
