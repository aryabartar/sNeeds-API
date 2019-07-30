from django.http import Http404
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, generics, mixins, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers
from .permissions import UserFileOwnerPermission


class CountryDetail(generics.RetrieveAPIView):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    lookup_field = 'slug'


class CountryList(generics.ListAPIView):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer


class UniversityDetail(generics.RetrieveAPIView):
    queryset = models.University.objects.all()
    serializer_class = serializers.UniversitySerializer
    lookup_field = 'slug'


class UniversityList(generics.ListAPIView):
    queryset = models.University.objects.all()
    serializer_class = serializers.UniversitySerializer


class FieldOfStudyDetail(generics.RetrieveAPIView):
    queryset = models.FieldOfStudy.objects.all()
    serializer_class = serializers.FieldOfStudySerializer
    lookup_field = 'slug'


class FieldOfStudyList(generics.ListAPIView):
    queryset = models.FieldOfStudy.objects.all()
    serializer_class = serializers.FieldOfStudySerializer


class ConsultantProfileDetail(APIView):
    def get_object(self, slug):
        try:
            return models.ConsultantProfile.objects.get(slug=slug)
        except models.FieldOfStudy.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        consultant_profile = self.get_object(slug)
        serializer = serializers.ConsultantProfileSerializer(consultant_profile, context={"request": request})
        return Response(serializer.data)


class ConsultantProfileList(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = models.ConsultantProfile.objects.all()
    serializer_class = serializers.ConsultantProfileSerializer
    filterset_fields = ('universities', 'field_of_studies', 'countries')

    def get_queryset(self):
        return models.ConsultantProfile.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MyAccountInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        consultant = None
        try:
            consultant = request.user.consultant_profile
        except:
            pass

        if consultant:
            is_consultant = True
            consultant_id = consultant.id
        else:
            is_consultant = False
            consultant_id = None

        return Response(
            {
                "user_pk": request.user.pk,
                "is_consultant": is_consultant,
                "consultant": consultant_id
            },
            200)


class UserFileListView(generics.ListCreateAPIView):
    queryset = models.UserFile.objects.all()
    serializer_class = serializers.UserFileSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        consultant_profile_qs = models.ConsultantProfile.objects.filter(user=user)
        if consultant_profile_qs.exists():
            return models.UserFile.objects.get_consultant_accessed_files(consultant_profile_qs.first())
        else:
            return models.UserFile.objects.filter(user=user)


class UserFileDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = models.UserFile.objects.all()
    serializer_class = serializers.UserFileSerializer
    permission_classes = [UserFileOwnerPermission, permissions.IsAuthenticated, ]
