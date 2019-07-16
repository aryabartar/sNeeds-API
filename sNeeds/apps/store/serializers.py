from rest_framework import serializers

from . import models


class TimeSlotSaleSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True, lookup_field='id',
                                               view_name="store:time-slot-sale-detail")

    consultant_url = serializers.HyperlinkedRelatedField(
        source='consultant',
        lookup_field='slug',
        read_only=True,
        view_name='account:consultant-profile-detail'
    )

    consultant_slug = serializers.SlugRelatedField(
        source='consultant',
        slug_field='slug',
        read_only=True
    )

    class Meta:
        model = models.TimeSlotSale
        fields = ('url', 'consultant', 'consultant_url', 'consultant_slug', 'start_time', 'end_time', 'price',)
