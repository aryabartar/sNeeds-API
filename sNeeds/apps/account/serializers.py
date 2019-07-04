from rest_framework import serializers
from . import models


class CountrySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="country-detail", lookup_field='slug')

    class Meta:
        model = models.Country
        fields = ('url', 'name',)
