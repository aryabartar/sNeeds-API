from rest_framework import serializers

import sNeeds.apps
from sNeeds.apps.account.serializers import UniversitySerializer, FieldOfStudySerializer, CountrySerializer
from sNeeds.apps.comments.models import SoldTimeSlotRate
from sNeeds.apps.consultants.models import StudyInfo, Country, FieldOfStudy, University


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
    universities2 = serializers.SerializerMethodField()
    field_of_studies = FieldOfStudySerializer(many=True, read_only=True)
    field_of_studies2 = serializers.SerializerMethodField()
    countries = CountrySerializer(many=True, read_only=True)
    countries2 = serializers.SerializerMethodField()

    class Meta:
        model = sNeeds.apps.consultants.models.ConsultantProfile
        fields = (
            'id', 'url', 'bio', 'profile_picture', 'first_name', 'last_name',
            'universities', 'universities2', 'field_of_studies', 'field_of_studies2', 'countries',  'countries2',
            'slug', 'aparat_link',
            'resume', 'rate', 'active')

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_rate(self, obj):
        if obj.rate is None:
            return None
        return '{0:g}'.format(round(obj.rate, 2))

    def get_field_of_studies2(self, obj):
        qs = StudyInfo.objects.filter(consultant=obj)
        field_of_studies_id = [s.field_of_study.id for s in qs]
        qs = FieldOfStudy.objects.filter(id__in=field_of_studies_id)
        return FieldOfStudySerializer(qs, many=True, read_only=True, context=self.context).data

    def get_countries2(self, obj):
        qs = StudyInfo.objects.filter(consultant=obj)
        countries_id = [s.country.id for s in qs]
        qs = Country.objects.filter(id__in=countries_id)
        return CountrySerializer(qs, many=True, read_only=True, context=self.context).data

    def get_universities2(self, obj):
        qs = StudyInfo.objects.filter(consultant=obj)
        universities_id = [s.university.id for s in qs]
        qs = University.objects.filter(id__in=universities_id)
        return CountrySerializer(qs, many=True, read_only=True, context=self.context).data


class ConsultantProfileDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="consultant:consultant-profile-detail",
        lookup_field='slug',
        read_only=True
    )
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    rate = serializers.SerializerMethodField()

    study_info = serializers.SerializerMethodField()

    class Meta:
        model = sNeeds.apps.consultants.models.ConsultantProfile
        fields = (
            'id', 'url', 'bio', 'profile_picture', 'first_name', 'last_name', 'study_info',
            'slug', 'aparat_link',
            'resume', 'rate', 'active')

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_rate(self, obj):
        if obj.rate is None:
            return None
        return '{0:g}'.format(round(obj.rate, 2))

    def get_study_info(self, obj):
        qs = StudyInfo.objects.filter(consultant=obj)
        return StudyInfoSerializer(qs, many=True, read_only=True, context=self.context).data


class StudyInfoSerializer(serializers.ModelSerializer):

    university = UniversitySerializer(read_only=True)
    field_of_study = FieldOfStudySerializer(read_only=True)
    country = CountrySerializer(read_only=True)

    class Meta:
        model = sNeeds.apps.consultants.models.StudyInfo
        fields = ('id', 'university', 'field_of_study', 'country', 'grade')

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_rate(self, obj):
        if obj.rate is None:
            return None
        return '{0:g}'.format(round(obj.rate, 2))

