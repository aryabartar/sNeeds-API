from django.http import Http404

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response

from . import serializers
from . import filtersets
from .models import TimeSlotSale, SoldTimeSlotSale
from .permissions import (
    ConsultantPermission,
    TimeSlotSaleOwnerPermission,
    SoldTimeSlotSaleOwnerPermission,
)

from sNeeds.apps.account.models import ConsultantProfile


class TimeSlotSailList(generics.ListCreateAPIView):
    queryset = TimeSlotSale.objects.all()
    serializer_class = serializers.TimeSlotSaleSerializer
    filterset_class = filtersets.TimeSlotSaleFilter
    permission_classes = [ConsultantPermission, permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SoldTimeSlotSailList(generics.ListAPIView):
    queryset = SoldTimeSlotSale.objects.all()
    serializer_class = serializers.SoldTimeSlotSaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        consultant_profile_qs = ConsultantProfile.objects.filter(user=user)

        if consultant_profile_qs.exists():
            consultant_profile = consultant_profile_qs.first()
            return SoldTimeSlotSale.objects.filter(consultant=consultant_profile)
        else:
            return SoldTimeSlotSale.objects.filter(sold_to=user)


class TimeSlotSaleDetail(generics.RetrieveDestroyAPIView):
    lookup_field = "id"
    queryset = TimeSlotSale.objects.all()
    serializer_class = serializers.TimeSlotSaleSerializer
    permission_classes = [TimeSlotSaleOwnerPermission, permissions.IsAuthenticatedOrReadOnly]


class SoldTimeSlotSailDetail(generics.RetrieveAPIView):
    lookup_field = "id"
    queryset = SoldTimeSlotSale.objects.all()
    serializer_class = serializers.SoldTimeSlotSaleSerializer
    permission_classes = [SoldTimeSlotSaleOwnerPermission, permissions.IsAuthenticated]
