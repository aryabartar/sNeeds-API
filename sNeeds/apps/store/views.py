from django.http import Http404

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response

from . import models
from . import serializers
from . import filtersets
from .permissions import ConsultantPermission


class TimeSlotSailList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.TimeSlotSale.objects.all()
    serializer_class = serializers.TimeSlotSaleSerializer
    filterset_class = filtersets.TimeSlotSailFilter
    permission_classes = [ConsultantPermission, permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.data
        consultant = request.user.consultant_profile
        try:
            data.pop('consultant')
        except:
            pass

        data.update({'consultant': consultant.pk})

        serializer = serializers.TimeSlotSaleSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
