from rest_framework import serializers
from .models import WebinarTimeSlot, Webinar, SoldWebinar


class WebinarSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField()

    class Meta:
        model = Webinar
        fields = ['id', '']


class SoldWebinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoldWebinar
