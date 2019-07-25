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
        return SoldTimeSlotSale.objects.filter(sold_to=self.request.user)


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
