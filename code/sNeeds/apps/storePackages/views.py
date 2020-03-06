from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import StorePackagePhase, StorePackage, StorePackagePhaseThrough


class StorePackagePhaseThroughListAPIView(generics.ListAPIView):
    queryset = StorePackagePhaseThrough.objects.all()
    serializer_class = serializers.StorePackageDetailPhaseThroughSerializer
    lookup_field = 'slug'
    filterset_fields = ['store_package']


class StorePackagePhaseThroughDetailAPIView(generics.RetrieveAPIView):
    queryset = StorePackagePhaseThrough.objects.all()
    serializer_class = serializers.StorePackageDetailPhaseThroughSerializer
    lookup_field = 'slug'
