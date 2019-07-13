from rest_framework import serializers

from . import models


class TimeSlotSaleSerializer(serializers.ModelSerializer):
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
        fields = ('consultant', 'consultant_url', 'consultant_slug', 'start_time', 'end_time', 'price',)
