from django.shortcuts import render
from django.http import Http404

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

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


class CountryList(generics.ListCreateAPIView):
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
