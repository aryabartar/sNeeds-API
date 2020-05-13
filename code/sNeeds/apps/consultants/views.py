from django.http import Http404
from django.shortcuts import render
from django.db.models import F

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, filters, pagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.consultants.serializers import ConsultantProfileSerializer
from .filters import ConsultantProfileFilter
from .paginators import StandardResultsSetPagination


class ConsultantProfileDetail(APIView):
    def get_object(self, slug):
        try:
            return ConsultantProfile.objects.get(slug=slug)
        except ConsultantProfile.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        consultant_profile = self.get_object(slug)
        serializer = ConsultantProfileSerializer(
            consultant_profile,
            context={"request": request}
        )
        return Response(serializer.data)


class ConsultantProfileList(generics.ListAPIView):
    serializer_class = ConsultantProfileSerializer
    pagination_class = StandardResultsSetPagination
    ordering_fields = []

    def get_queryset(self):
        qs = ConsultantProfile.objects.filter(active=True).at_least_one_time_slot()

        university = self.request.query_params.getlist("university")
        country = self.request.query_params.getlist("country")
        field_of_study = self.request.query_params.getlist("field_of_study")

        if university != [] or country != [] or field_of_study != []:
            qs_for_university = qs.none()
            qs_for_country = qs.none()
            qs_for_field_of_study = qs.none()

            if university is not None:
                qs_for_university = qs.filter_consultants({"universities": university})

            if country is not None:
                qs_for_country = qs.filter_consultants({"countries": country})

            if field_of_study is not None:
                qs_for_field_of_study = qs.filter_consultants({"field_of_studies": field_of_study})

            qs = qs_for_university | qs_for_country | qs_for_field_of_study
            qs = qs.distinct()

        if self.request.query_params.get("ordering") is not None:
            if "-rate" in self.request.query_params.get("ordering"):
                qs = qs.order_by(F('rate').desc(nulls_last=True))
            elif "rate" in self.request.query_params.get("ordering"):
                qs = qs.order_by(F('rate').asc(nulls_first=True))

        return qs
