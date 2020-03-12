from rest_framework import serializers
from .models import Webinar, SoldWebinar
from ..customAuth.serializers import SafeUserDataSerializer


class WebinarSerializer(serializers.ModelSerializer):
    # sold = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     lookup_field='slug',
    #     view_name='webinars:webinar-detail'
    # )

    class Meta:
        model = Webinar
        fields = ('id', 'title', 'slug', 'active')

        extra_kwargs = {
            'id': {'read_only': True},
            'slug': {'read_only': True},
        }


class SoldWebinarSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='id',
        view_name="webinars:sold-webinar-detail",
        read_only=True
    )

    webinar = serializers.HyperlinkedRelatedField(
        read_only=True,
        lookup_field='slug',
        view_name='webinars:webinar-detail'
    )

    sold_to = serializers.SerializerMethodField()

    class Meta:
        model = SoldWebinar
        fields = [
            'id', 'url', 'webinar', 'price', 'sold_to',
        ]

    def get_sold_to(self, obj):
        return SafeUserDataSerializer(obj.sold_to).data
