from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import StorePackagePhase, StorePackage, StorePackagePhaseThrough, ConsultantSoldStorePackageAcceptRequest
from sNeeds.utils.custom import custom_permissions
from ..consultants.models import ConsultantProfile
from .permissions import ConsultantSoldStorePackageAcceptRequestViewPermission


class StorePackagePhaseThroughListAPIView(generics.ListAPIView):
    queryset = StorePackagePhaseThrough.objects.all()
    serializer_class = serializers.StorePackagePhaseThroughSerializer
    filterset_fields = ['store_package']


class StorePackagePhaseThroughDetailAPIView(generics.RetrieveAPIView):
    queryset = StorePackagePhaseThrough.objects.all()
    serializer_class = serializers.StorePackagePhaseThroughSerializer
    lookup_field = 'id'


class StorePackageListAPIView(generics.ListAPIView):
    queryset = StorePackage.objects.all()
    serializer_class = serializers.StorePackageSerializer


class StorePackageDetailAPIView(generics.RetrieveAPIView):
    queryset = StorePackage.objects.all()
    serializer_class = serializers.StorePackageSerializer
    lookup_field = 'slug'


class ConsultantSoldStorePackageAcceptRequestDetailAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = serializers.ConsultantSoldStorePackageAcceptRequestSerializer
    queryset = ConsultantSoldStorePackageAcceptRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated, ConsultantSoldStorePackageAcceptRequestViewPermission]


class ConsultantSoldStorePackageAcceptRequestListAPIView(generics.ListCreateAPIView):
    lookup_field = 'id'
    serializer_class = serializers.ConsultantSoldStorePackageAcceptRequestSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        is_consultant = ConsultantProfile.objects.filter(user=user).exists()

        if is_consultant:
            consultant = ConsultantProfile.objects.get(user=user)
            qs = ConsultantSoldStorePackageAcceptRequest.objects.filter(
                consultant=consultant
            )
        else:
            qs = ConsultantSoldStorePackageAcceptRequest.objects.filter(
                sold_store_package__sold_to=user
            )
        return qs
