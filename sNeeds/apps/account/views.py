from django.shortcuts import render
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from .models import Country, University, FieldOfStudy, ConsultantProfile
from . import  serializers


class CountryDetail(APIView):
    def get_object(self, slug):
        try:
            return Country.objects.get(slug=slug)
        except Country.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        country = self.get_object(slug)
        serializer = CountrySerializer(country, context={"request": request})
        return Response(serializer.data)


class UniversityDetail(APIView):
    def get_object(self, slug):
        try:
            return University.objects.get(slug=slug)
        except University.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        university = self.get_object(slug)
        serializer = serializers.UniversitySerializer(university, context={"request": request})
        return Response(serializer.data)
