from django.http import Http404

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response

from . import serializers
from . import filtersets
from .models import TimeSlotSale, SoldTimeSlotSale, Product
from .permissions import (
    ConsultantPermission,
    TimeSlotSaleOwnerPermission,
    SoldTimeSlotSaleOwnerPermission,
)

from sNeeds.apps.customAuth.models import ConsultantProfile


class TimeSlotSailList(generics.ListCreateAPIView):
    queryset = TimeSlotSale.objects.all()
    serializer_class = serializers.TimeSlotSaleSerializer
    filterset_class = filtersets.TimeSlotSaleFilter
    permission_classes = [ConsultantPermission, permissions.IsAuthenticatedOrReadOnly]


class SoldTimeSlotSaleList(generics.ListAPIView):
    queryset = SoldTimeSlotSale.objects.all()
    serializer_class = serializers.SoldTimeSlotSaleSerializer
    filterset_fields = ['used', ]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        consultant_profile_qs = ConsultantProfile.objects.filter(user=user)

        if consultant_profile_qs.exists():
            consultant_profile = consultant_profile_qs.first()
            return SoldTimeSlotSale.objects.filter(consultant=consultant_profile).order_by('-start_time')
        else:
            return SoldTimeSlotSale.objects.filter(sold_to=user).order_by('-start_time')


class TimeSlotSaleDetail(generics.RetrieveDestroyAPIView):
    lookup_field = "id"
    queryset = TimeSlotSale.objects.all()
    serializer_class = serializers.TimeSlotSaleSerializer
    permission_classes = [TimeSlotSaleOwnerPermission, permissions.IsAuthenticatedOrReadOnly]


class SoldTimeSlotSaleDetail(generics.RetrieveAPIView):
    lookup_field = "id"
    queryset = SoldTimeSlotSale.objects.all()
    serializer_class = serializers.SoldTimeSlotSaleSerializer
    permission_classes = [SoldTimeSlotSaleOwnerPermission, permissions.IsAuthenticated]
