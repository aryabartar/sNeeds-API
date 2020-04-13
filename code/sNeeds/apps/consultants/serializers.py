from rest_framework import serializers

import sNeeds.apps
from sNeeds.apps.account.serializers import UniversitySerializer, FieldOfStudySerializer, CountrySerializer
from sNeeds.apps.comments.models import SoldTimeSlotRate
from sNeeds.apps.consultants.models import StudyInfo, Country, FieldOfStudy, University, ConsultantProfile


class ShortConsultantProfileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="consultant:consultant-profile-detail",
        lookup_field='slug',
        read_only=True
    )
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = sNeeds.apps.consultants.models.ConsultantProfile
        fields = (
            'id',
            'url',
            'profile_picture',
            'first_name',
            'last_name',
        )

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name


class ConsultantProfileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="consultant:consultant-profile-detail",
        lookup_field='slug',
        read_only=True
    )
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    rate = serializers.SerializerMethodField()

    universities = UniversitySerializer(many=True, read_only=True)
    field_of_studies = FieldOfStudySerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)
    study_info = serializers.SerializerMethodField()

    # TODO: After deploy
    # update fields for move to StudyInfo approach
    class Meta:
        model = ConsultantProfile
        fields = (
            'id', 'url', 'bio', 'profile_picture', 'first_name', 'last_name',
            'universities', 'field_of_studies', 'countries', 'study_info',
            'slug', 'aparat_link', 'resume', 'time_slot_price', 'rate', 'active')

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_rate(self, obj):
        if obj.rate is None:
            return None
        return '{0:g}'.format(round(obj.rate, 2))

    def get_study_info(self, obj):
        qs = StudyInfo.objects.filter(consultant__id=obj.id)
        return StudyInfoSerializer(qs, many=True, context=self.context).data


class StudyInfoSerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    field_of_study = FieldOfStudySerializer(read_only=True)
    country = CountrySerializer(read_only=True)

    class Meta:
        model = sNeeds.apps.consultants.models.StudyInfo
        fields = ('id', 'university', 'field_of_study', 'country', 'grade')
