from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import StorePackagePhase, StorePackage


class StorePackageDetailPhaseThroughListAPIView(generics.ListAPIView):
    queryset = StorePackagePhase.objects.all()
    serializer_class = serializers.StorePackageDetailPhaseThroughSerializer
    lookup_field = 'slug'
    filterset_fields = ['']


class StorePackageDetailPhaseThroughDetailAPIView(generics.RetrieveAPIView):
    queryset = StorePackagePhase.objects.all()
    serializer_class = serializers.StorePackageDetailPhaseThroughSerializer
    lookup_field = 'slug'
