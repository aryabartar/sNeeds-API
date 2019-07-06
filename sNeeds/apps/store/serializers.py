from rest_framework import serializers

from . import models


class TimeSlotSaleSerializer(serializers.ModelSerializer):
    consultant = serializers.HyperlinkedRelatedField(
        lookup_field='slug',
        read_only=True,
        view_name='account:consultant-profile-detail'
    )

    class Meta:
        model = models.TimeSlotSale
        fields = ('consultant',  'start_time', 'end_time', 'price',)
