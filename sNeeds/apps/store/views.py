from django.http import Http404

from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from . import models
from . import serializers
from . import utils
from . import filtersets


class TimeSlotSailList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.TimeSlotSale.objects.all()
    serializer_class = serializers.TimeSlotSaleSerializer
    filterset_class = filtersets.TimeSlotSailFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.data
        consultant = request.user.consultant_profile
        data.update({'consultant': consultant.pk})

        serializer = serializers.TimeSlotSaleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({}, 200)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
