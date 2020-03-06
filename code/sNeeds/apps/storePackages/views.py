from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import StorePackageDetailPhase


class StorePackageDetailPhaseDetailView(generics.RetrieveAPIView):
    queryset = StorePackageDetailPhase.objects.all()
    serializer_class = serializers.StorePackageDetailPhaseSerializer
    lookup_field = 'slug'
