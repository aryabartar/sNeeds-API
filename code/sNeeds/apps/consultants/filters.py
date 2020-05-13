from django.db.models import Q
from django_filters.rest_framework import filters, FilterSet
# import django_filters
from .models import StudyInfo, ConsultantProfile
from sNeeds.apps.account.models import University, Country, FieldOfStudy


class UniversityModelMultipleChoiceFilter(filters.ModelMultipleChoiceFilter):

    def filter(self, qs, value):
        if not value:
            # Even though not a noop, no point filtering if empty.
            return qs

        if self.is_noop(qs, value):
            return qs

        q = Q()
        for v in set(value):
            if v == self.null_value:
                v = None
            if v is not None:
                q = q | Q(university=v)

        study_info_qs = StudyInfo.objects.filter(q).only('consultant')

        consultants_id = []
        for c in study_info_qs:
            consultants_id.append(c.consultant.id)

        qs = qs.filter(id__in=consultants_id)

        return qs.distinct()


class CountryModelMultipleChoiceFilter(filters.ModelMultipleChoiceFilter):

    def filter(self, qs, value):
        if not value:
            # Even though not a noop, no point filtering if empty.
            return qs

        if self.is_noop(qs, value):
            return qs

        q = Q()
        for v in set(value):
            if v == self.null_value:
                v = None
            if v is not None:
                q |= Q(university__country=v)

        study_info_qs = StudyInfo.objects.filter(q).only('consultant')

        consultants_id = []
        for c in study_info_qs:
            consultants_id.append(c.consultant.id)

        qs = qs.filter(id__in=consultants_id)

        return qs.distinct()


class FieldOfStudyModelMultipleChoiceFilter(filters.ModelMultipleChoiceFilter):

    def filter(self, qs, value):
        if not value:
            # Even though not a noop, no point filtering if empty.
            return qs

        if self.is_noop(qs, value):
            return qs

        q = Q()
        for v in set(value):
            if v == self.null_value:
                v = None
            if v is not None:
                q |= Q(field_of_study=v)

        study_info_qs = StudyInfo.objects.filter(q).only('consultant')

        consultants_id = []
        for c in study_info_qs:
            consultants_id.append(c.consultant.id)

        qs = qs.filter(id__in=consultants_id)

        return qs.distinct()


class ConsultantProfileFilter(FilterSet):
    university = UniversityModelMultipleChoiceFilter(
        field_name='university', queryset=University.objects.all(), label='university'
    )

    country = CountryModelMultipleChoiceFilter(
        field_name='country', queryset=Country.objects.all(), label='country'
    )

    field_of_study = FieldOfStudyModelMultipleChoiceFilter(
        field_name='field_of_study', queryset=FieldOfStudy.objects.all(), label='field_of_study'
    )

    class Meta:
        model = ConsultantProfile
        fields = ['active']
