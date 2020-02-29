from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

import sNeeds.apps
from sNeeds.apps.consultants.models import ConsultantProfile


class ConsultantProfileDetail(APIView):
    def get_object(self, slug):
        try:
            return ConsultantProfile.objects.get(slug=slug)
        except ConsultantProfile.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        consultant_profile = self.get_object(slug)
        serializer = sNeeds.apps.consultants.serializers.ConsultantProfileSerializer(consultant_profile, context={"request": request})
        return Response(serializer.data)


class ConsultantProfileList(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = ConsultantProfile.objects.all()
    serializer_class = sNeeds.apps.consultants.serializers.ConsultantProfileSerializer
    filterset_fields = ('universities', 'field_of_studies', 'countries')

    def get_queryset(self):
        return ConsultantProfile.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)