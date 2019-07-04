from django.shortcuts import render
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from .models import  Country
from .serializers import CountrySerializer


class CountryDetail(APIView):
    def get_object(self, slug):
        try:
            return Country.objects.get(slug=slug)
        except Country.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        country = self.get_object(slug)
        serializer = CountrySerializer(country)
        return Response(serializer.data)