from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models
from sNeeds.apps.comments.models import SoldTimeSlotRate

User = get_user_model()


class CountrySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="account:country-detail", lookup_field='slug', read_only=True)

    class Meta:
        model = models.Country
        fields = ('id', 'url', 'name', 'slug', 'picture')


class UniversitySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="account:university-detail", lookup_field='slug',
                                               read_only=True)

    class Meta:
        model = models.University
        fields = ('id', 'url', 'name', 'country', 'description', 'slug', 'picture')


class FieldOfStudySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="account:field-of-study-detail", lookup_field='slug',
                                               read_only=True)

    class Meta:
        model = models.FieldOfStudy
        fields = ('id', 'url', 'name', 'description', 'slug', 'picture')


class ConsultantProfileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account:consultant-profile-detail",
        lookup_field='slug',
        read_only=True
    )
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    rate = serializers.SerializerMethodField(read_only=True)

    universities = UniversitySerializer(many=True, read_only=True)
    field_of_studies = FieldOfStudySerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)

    class Meta:
        model = models.ConsultantProfile
        fields = (
            'id', 'url', 'bio', 'profile_picture', 'first_name', 'last_name',
            'universities', 'field_of_studies', 'countries', 'slug', 'aparat_link',
             'resume','rate', 'active')

    def get_rate(self, obj):
        qs = SoldTimeSlotRate.objects.filter(sold_time_slot__consultant=obj)

        if not qs.exists():
            return None

        sum = 0
        for obj in qs:
            sum += obj.rate
        avg = sum / qs.count()

        return avg

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name
