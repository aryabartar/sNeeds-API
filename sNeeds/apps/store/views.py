from django.http import Http404

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response

from . import models
from . import serializers
from . import filtersets
from .permissions import ConsultantPermission


class TimeSlotSailList(generics.ListCreateAPIView):
    queryset = models.TimeSlotSale.objects.all()
    serializer_class = serializers.TimeSlotSaleSerializer
    filterset_class = filtersets.TimeSlotSailFilter
    permission_classes = [ConsultantPermission, permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TimeSlotSaleDetail(generics.RetrieveAPIView):
    queryset = models.TimeSlotSale.objects.all()
    serializer_class = serializers.TimeSlotSaleSerializer
    lookup_field = "id"
