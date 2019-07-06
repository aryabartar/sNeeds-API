from django.http import Http404

from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from . import models
from . import serializers
from . import utils

from sNeeds.apps.account.models import ConsultantProfile


class TimeSlotSailList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.TimeSlotSale.objects.all()
    serializer_class = serializers.TimeSlotSaleSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if utils.is_consultant(user):
            return models.TimeSlotSale.objects.filter(consultant__user__exact=user)
        else:
            return models.TimeSlotSale.objects.filter(buyer__exact=user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
