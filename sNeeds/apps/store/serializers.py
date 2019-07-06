from rest_framework import serializers

from . import models


class TimeSlotSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TimeSlotSale
        fields = ('consultant', 'start_time', 'end_time', 'price',)
