from rest_framework import serializers
from .models import WebinarTimeSlot, Webinar


class WebinarTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebinarTimeSlot
        fields = ['id', '']


class WebinarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Webinar