from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models

User = get_user_model()


def validate_user_password(password):
    try:
        # validate the password and catch the exception
        validators.validate_password(password)

    # the exception raised here is different than serializers.ValidationError
    except exceptions.ValidationError as e:
        raise serializers.ValidationError(e.messages)


class CountrySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="account:country-detail", lookup_field='slug', read_only=True)

    class Meta:
        model = models.Country
        fields = ('url', 'name', 'slug')


class UniversitySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="account:university-detail", lookup_field='slug',
                                               read_only=True)

    class Meta:
        model = models.University
        fields = ('url', 'name', 'country', 'description', 'slug')


class FieldOfStudySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="account:field-of-study-detail", lookup_field='slug',
                                               read_only=True)

    class Meta:
        model = models.FieldOfStudy
        fields = ('url', 'name', 'description', 'slug')


class ConsultantProfileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account:consultant-profile-detail",
        lookup_field='slug',
        read_only=True
    )

    universities = UniversitySerializer(many=True, read_only=True)
    field_of_studies = FieldOfStudySerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)

    class Meta:
        model = models.ConsultantProfile
        fields = ('url', 'pk', 'user', 'universities', 'field_of_studies', 'countries', 'slug', 'aparat_link')


