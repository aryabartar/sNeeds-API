from django.http import Http404

from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from . import models
from . import serializers
from . import utils


class TimeSlotSailList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.TimeSlotSale.objects.all()
    serializer_class = serializers.TimeSlotSaleSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('consultant',)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
