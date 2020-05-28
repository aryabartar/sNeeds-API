from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import ValidationError
from . import models
from .models import StudentDetailedInfo, StudentFormFieldsChoice, StudentFormApplySemesterYear

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


class StudentFormFieldsChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentFormFieldsChoice
        fields = [
            'id', 'name', 'category', 'slug'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'read_only': True},
            'category': {'read_only': False},
            'slug': {'read_only': False},
        }


class StudentFormFieldsChoiceCustomPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_choices(self, cutoff=None):
        """
        This method is overridden.
        Issue was:
        https://stackoverflow.com/questions/50973569/django-rest-framework-relatedfield-cant-return-a-dict-object
        """
        queryset = self.get_queryset()
        if queryset is None:
            # Ensure that field.choices returns something sensible
            # even when accessed with a read-only field.
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])

    def to_representation(self, value):
        obj = StudentFormFieldsChoice.objects.get(pk=value.pk)
        return StudentFormFieldsChoiceSerializer(obj).data


class StudentFormApplySemesterYearSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentFormApplySemesterYear
        fields = ['id', 'year', 'semester']


class StudentFormApplySemesterYearCustomPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_choices(self, cutoff=None):
        """
        This method is overridden.
        Issue was:
        https://stackoverflow.com/questions/50973569/django-rest-framework-relatedfield-cant-return-a-dict-object
        """
        queryset = self.get_queryset()
        if queryset is None:
            # Ensure that field.choices returns something sensible
            # even when accessed with a read-only field.
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])

    def to_representation(self, value):
        obj = StudentFormApplySemesterYear.objects.get(pk=value.pk)
        return StudentFormApplySemesterYearSerializer(obj).data


class StudentDetailedInfoSerializer(serializers.ModelSerializer):
    from sNeeds.apps.customAuth.serializers import SafeUserDataSerializer
    user = SafeUserDataSerializer(read_only=True)

    grade \
        = StudentFormFieldsChoiceCustomPrimaryKeyRelatedField(queryset=StudentFormFieldsChoice.objects.all())
    major \
        = StudentFormFieldsChoiceCustomPrimaryKeyRelatedField(queryset=StudentFormFieldsChoice.objects.all())
    university \
        = StudentFormFieldsChoiceCustomPrimaryKeyRelatedField(queryset=StudentFormFieldsChoice.objects.all())
    apply_grade \
        = StudentFormFieldsChoiceCustomPrimaryKeyRelatedField(queryset=StudentFormFieldsChoice.objects.all())
    apply_major \
        = StudentFormFieldsChoiceCustomPrimaryKeyRelatedField(queryset=StudentFormFieldsChoice.objects.all())
    apply_country \
        = StudentFormFieldsChoiceCustomPrimaryKeyRelatedField(queryset=StudentFormFieldsChoice.objects.all())
    apply_mainland \
        = StudentFormFieldsChoiceCustomPrimaryKeyRelatedField(queryset=StudentFormFieldsChoice.objects.all())
    marital_status \
        = StudentFormFieldsChoiceCustomPrimaryKeyRelatedField(queryset=StudentFormFieldsChoice.objects.all())
    apply_university \
        = StudentFormFieldsChoiceCustomPrimaryKeyRelatedField(queryset=StudentFormFieldsChoice.objects.all())
    language_certificate \
        = StudentFormFieldsChoiceCustomPrimaryKeyRelatedField(queryset=StudentFormFieldsChoice.objects.all())
    degree_conferral_year \
        = StudentFormFieldsChoiceCustomPrimaryKeyRelatedField(queryset=StudentFormFieldsChoice.objects.all())

    apply_semester_year \
        = StudentFormApplySemesterYearCustomPrimaryKeyRelatedField(many=False,
                                                                   queryset=StudentFormApplySemesterYear.objects.all())

    class Meta:
        model = StudentDetailedInfo
        fields = [
            'id', 'user', 'created', 'updated', 'age', 'marital_status', 'grade', 'university', 'degree_conferral_year',
            'major', 'total_average', 'thesis_title',
            'language_certificate', 'language_certificate_overall', 'language_speaking', 'language_listening',
            'language_writing', 'language_reading',
            'apply_mainland', 'apply_country', 'apply_grade', 'apply_major', 'apply_university',
            'apply_semester_year',
            'comment', 'resume']

        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
        }

    def validate(self, attrs):
        if attrs.get('grade').category != 'grade':
            raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}".format('grade', 'grade')))
        if attrs.get('major').category != 'major':
            raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}".format('major', 'major')))
        if attrs.get('university').category != 'university':
            raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}".format('university',
                                                                                                      'university')))
        if attrs.get('apply_grade').category != 'apply_grade':
            raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}".format('apply_grade',
                                                                                                      'apply_grade')))
        if attrs.get('apply_major').category != 'apply_major':
            raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}".format('apply_major',
                                                                                                      'apply_major')))
        if attrs.get('apply_country').category != 'apply_country':
            raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}".format('apply_country',
                                                                                                      'apply_country')))
        if attrs.get('apply_mainland').category != 'apply_mainland':
            raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}".format('apply_mainland',
                                                                                                      'apply_mainland')))
        if attrs.get('marital_status').category != 'marital_status':
            raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}".format('marital_status',
                                                                                                      'marital_status')))
        if attrs.get('apply_university').category != 'apply_university':
            raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}".format('apply_university',
                                                                                                      'apply_university')))
        if attrs.get('language_certificate').category != 'language_certificate':
            raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}".format('language_certificate',
                                                                                                      'language_certificate')))
        if attrs.get('degree_conferral_year').category != 'degree_conferral_year':
            raise ValidationError(_("The Value Entered for: {} is not in allowed category: {}".format('degree_conferral_year',
                                                                                                      'degree_conferral_year')))
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        user_student_detailed_info_qs = StudentDetailedInfo.objects.filter(user=user)
        if user_student_detailed_info_qs.exists():
            raise ValidationError(_("User already has student detailed info"))
        student_detailed_info_obj = StudentDetailedInfo.objects.create(user=user, **validated_data)
        return student_detailed_info_obj

