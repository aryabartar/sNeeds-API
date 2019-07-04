from rest_framework import serializers
from . import models


class CountrySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="country-detail", lookup_field='slug', read_only=True)

    class Meta:
        model = models.Country
        fields = ('url', 'name', 'slug')


class UniversitySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="university-detail", lookup_field='slug', read_only=True)

    class Meta:
        model = models.University
        fields = ('url', 'name', 'country', 'description', 'slug')


class FieldOfStudySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="field-of-study-detail", lookup_field='slug', read_only=True)

    class Meta:
        model = models.FieldOfStudy
        fields = ('url', 'name',  'description', 'slug')
