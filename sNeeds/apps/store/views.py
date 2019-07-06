from django.http import Http404

from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers


class TimeSlotSailList(generics.GenericAPIView):
    queryset = models.TimeSlotSale.objects.all()
    serializer_class = serializers.TimeSlotSaleSerializer

    def get_queryset(self):
        user = self.request.user
        return models.TimeSlotSale.objects.filter()
