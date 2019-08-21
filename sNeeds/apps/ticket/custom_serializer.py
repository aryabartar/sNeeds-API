from rest_framework import serializers as drf_serializer

from sNeeds.apps.account.serializers import ConsultantProfileSerializer
from sNeeds.apps.account.models import ConsultantProfile


class ConsultantSerializer(drf_serializer.Field):
    def to_representation(self, value):
        return ConsultantProfileSerializer(value, context={'request': self.context['request']}).data

    def to_internal_value(self, id):
        try:
            id = int(id)
        except ValueError:
           raise drf_serializer.ValidationError("Provide id of consultant in numbers, please.")
        try:
            consultant = ConsultantProfile.objects.get(pk=id)
        except ConsultantProfile.DoesNotExist:
            raise drf_serializer.ValidationError("Such a consultant does not exist")
        return consultant