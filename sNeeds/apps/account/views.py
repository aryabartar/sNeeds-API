from django.shortcuts import render
from django.http import Http404

from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from django_filtes
from . import models
from . import serializers


class CountryDetail(APIView):
    def get_object(self, slug):
        try:
            return models.Country.objects.get(slug=slug)
        except models.Country.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        country = self.get_object(slug)
        serializer = serializers.CountrySerializer(country, context={"request": request})
        return Response(serializer.data)


class CountryList(generics.ListAPIView):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer


class UniversityDetail(APIView):
    def get_object(self, slug):
        try:
            return models.University.objects.get(slug=slug)
        except models.University.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        university = self.get_object(slug)
        serializer = serializers.UniversitySerializer(university, context={"request": request})
        return Response(serializer.data)


class UniversityList(generics.ListAPIView):
    queryset = models.University.objects.all()
    serializer_class = serializers.UniversitySerializer


class FieldOfStudyDetail(APIView):
    def get_object(self, slug):
        try:
            return models.FieldOfStudy.objects.get(slug=slug)
        except models.FieldOfStudy.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        field_of_study = self.get_object(slug)
        serializer = serializers.FieldOfStudySerializer(field_of_study, context={"request": request})
        return Response(serializer.data)


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
    queryset = models.FieldOfStudy.objects.all()
    serializer_class = serializers.FieldOfStudySerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    def get_queryset(self):
        print(self.request.query_params)
        return models.FieldOfStudy.objects.all()

    def get(self, request , *args, **kwargs):
        return self.list(request, *args, **kwargs)