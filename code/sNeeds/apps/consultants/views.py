from django.http import Http404
from django.shortcuts import render

# Create your views here.
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
from ..store.models import TimeSlotSale


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


def get_rate(obj):
    if obj.rate is None:
        return 0
    return obj.rate


class ConsultantProfileList(generics.ListAPIView):
    serializer_class = ConsultantProfileSerializer
    # ordering_fields = ['rate', 'created', ]
    pagination_class = StandardResultsSetPagination
    filterset_class = ConsultantProfileFilter

    def get_queryset(self):
        qs = ConsultantProfile.objects.filter(active=True).at_least_one_time_slot()

        returned_qs = ConsultantProfile.objects.none()
        for obj in qs:
            if TimeSlotSale.objects.filter(consultant=obj).exists():
                returned_qs |= ConsultantProfile.objects.filter(id=obj.id)
        returned_qs = sorted(returned_qs, key=get_rate, reverse=True)
        r_qs = ConsultantProfile.objects.none()
        for obj in returned_qs:
            r_qs |= ConsultantProfile.objects.filter(id=obj.id)
        print(r_qs)
        return r_qs
