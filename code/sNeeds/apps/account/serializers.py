from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import ValidationError

from . import models
from .models import StudentDetailedInfo
from sNeeds.utils.custom.custom_functions import student_info_year_choices, current_year

User = get_user_model()


# TODO: Move SoldTimeSlotRate

class CountrySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account:country-detail",
        lookup_field='slug',
        read_only=True
    )

    class Meta:
        model = models.Country
        fields = ('id', 'url', 'name', 'slug', 'picture')


class UniversitySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="account:university-detail", lookup_field='slug',
                                               read_only=True)
    country = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="account:country-detail",
        lookup_field='slug',
    )

    class Meta:
        model = models.University
        fields = ('id', 'url', 'name', 'country', 'description', 'slug', 'picture')


class FieldOfStudySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account:field-of-study-detail",
        lookup_field='slug',
        read_only=True
    )

    class Meta:
        model = models.FieldOfStudy
        fields = ('id', 'url', 'name', 'description', 'slug', 'picture')


class StudentDetailedInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentDetailedInfo
        fields = '__all__'
        exclude = ('user',)

        extra_kwargs = {
            'id': {'read_only': True},
        }

    def validate(self, attrs):
        student_info_conferral_year_choices = student_info_year_choices()
        degree_conferral_year = attrs.get('degree_conferral_year', None)
        if degree_conferral_year is None:
            attrs['degree_conferral_year'] = current_year()
        elif degree_conferral_year not in student_info_conferral_year_choices:
            raise ValidationError(_("Not valid degree conferral year"))
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        student_detailed_info_obj = StudentDetailedInfo.objects.create(user=user, **validated_data)
        return student_detailed_info_obj
