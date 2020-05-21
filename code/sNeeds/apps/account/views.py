from rest_framework import generics, permissions

from . import models
from . import serializers
# from .models import StudentDetailedInfo, StudentFormFieldsChoice, StudentFormApplySemesterYear
from .permissions import IsStudentPermission, StudentDetailedInfoOwnerOrInteractConsultantPermission
# from .serializers import StudentDetailedInfoSerializer, StudentFormFieldsChoiceSerializer,\
#     StudentFormApplySemesterYearSerializer


class CountryDetail(generics.RetrieveAPIView):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    lookup_field = 'slug'


class CountryList(generics.ListAPIView):
    serializer_class = serializers.CountrySerializer

    def get_queryset(self):
        from sNeeds.apps.consultants.models import StudyInfo
        study_info_with_active_consultant_qs = StudyInfo.objects.all().with_active_consultants()
        country_list = list(study_info_with_active_consultant_qs.values_list('university__country_id', flat=True))
        return models.Country.objects.filter(id__in=country_list).exclude(slug="iran")


class UniversityDetail(generics.RetrieveAPIView):
    queryset = models.University.objects.all()
    serializer_class = serializers.UniversitySerializer
    lookup_field = 'slug'


class UniversityList(generics.ListAPIView):
    serializer_class = serializers.UniversitySerializer

    def get_queryset(self):
        from sNeeds.apps.consultants.models import StudyInfo
        study_info_with_active_consultant_qs = StudyInfo.objects.all().with_active_consultants()
        university_list = list(study_info_with_active_consultant_qs.values_list('university_id', flat=True))
        return models.University.objects.filter(id__in=university_list)


class FieldOfStudyDetail(generics.RetrieveAPIView):
    queryset = models.FieldOfStudy.objects.all()
    serializer_class = serializers.FieldOfStudySerializer
    lookup_field = 'slug'


class FieldOfStudyList(generics.ListAPIView):
    serializer_class = serializers.FieldOfStudySerializer

    def get_queryset(self):
        from sNeeds.apps.consultants.models import StudyInfo
        study_info_with_active_consultant_qs = StudyInfo.objects.all().with_active_consultants()
        field_of_study_list = list(study_info_with_active_consultant_qs.values_list('field_of_study__id', flat=True))
        return models.FieldOfStudy.objects.filter(id__in=field_of_study_list)


# class StudentDetailedInfoListCreateAPIView(generics.ListCreateAPIView):
#     queryset = StudentDetailedInfo.objects.all()
#     serializer_class = StudentDetailedInfoSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStudentPermission)
#
#     def get_queryset(self):
#         user = self.request.user
#         qs = StudentDetailedInfo.objects.filter(user=user)
#         return qs
#
#
# class StudentDetailedInfoRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
#     lookup_field = 'id'
#     queryset = StudentDetailedInfo.objects.all()
#     serializer_class = StudentDetailedInfoSerializer
#     permission_classes = (permissions.IsAuthenticated, StudentDetailedInfoOwnerOrInteractConsultantPermission)
#
#
# class StudentFormFieldsChoiceListAPIView(generics.ListAPIView):
#     queryset = StudentFormFieldsChoice.objects.all()
#     serializer_class = StudentFormFieldsChoiceSerializer
#     filterset_fields = ['category']
#
#
# class StudentFormApplySemesterYearListAPIView(generics.ListAPIView):
#     queryset = StudentFormApplySemesterYear.objects.all()
#     serializer_class = StudentFormApplySemesterYearSerializer
