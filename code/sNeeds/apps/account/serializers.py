from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import ValidationError

from . import models
# from .models import StudentDetailedInfo, StudentFormFieldsChoice, StudentFormApplySemesterYear

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


# class StudentFormFieldsChoiceSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = StudentFormFieldsChoice
#         fields = ['id', 'name', 'category', 'slug']
#
#
# class StudentFormFieldsChoiceSerializerForShowInForm(serializers.ModelSerializer):
#
#     class Meta:
#         model = StudentFormFieldsChoice
#         fields = ['id']
#
#
# class StudentFormApplySemesterYearSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = StudentFormApplySemesterYear
#         fields = ['id', 'year', 'semester']
#
#
# class StudentDetailedInfoSerializer(serializers.ModelSerializer):
#     from sNeeds.apps.customAuth.serializers import SafeUserDataSerializer
#     user = SafeUserDataSerializer(read_only=True)
#     grade = StudentFormFieldsChoiceSerializerForShowInForm()
#     university = StudentFormFieldsChoiceSerializerForShowInForm()
#     degree_conferral_year = StudentFormFieldsChoiceSerializerForShowInForm()
#     major = StudentFormFieldsChoiceSerializerForShowInForm()
#     language_certificate = StudentFormFieldsChoiceSerializerForShowInForm()
#     apply_mainland = StudentFormFieldsChoiceSerializerForShowInForm()
#     apply_country = StudentFormFieldsChoiceSerializerForShowInForm()
#     apply_grade = StudentFormFieldsChoiceSerializerForShowInForm()
#     apply_major = StudentFormFieldsChoiceSerializerForShowInForm()
#     apply_university = StudentFormFieldsChoiceSerializerForShowInForm()
#
#     apply_semester_year = StudentFormApplySemesterYearSerializer()
#
#     class Meta:
#         model = StudentDetailedInfo
#         fields = '__all__'
#
#         extra_kwargs = {
#             'id': {'read_only': True},
#             'user': {'read_only': True},
#         }
#
#     def validate(self, attrs):
#         print(attrs.get('apply_country'))
#         return attrs
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         user = request.user
#         user_student_detailed_info_qs = StudentDetailedInfo.objects.filter(user=user)
#         if user_student_detailed_info_qs.exists():
#             raise ValidationError(_("User already has student detailed info"))
#         student_detailed_info_obj = StudentDetailedInfo.objects.create(user=user, **validated_data)
#         return student_detailed_info_obj
#
