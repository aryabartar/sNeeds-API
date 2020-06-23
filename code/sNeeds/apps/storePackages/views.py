from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response

from . import serializers
from .filters import SoldStorePackagePhaseDetailFilter
from .models import StorePackagePhase, StorePackage, StorePackagePhaseThrough, ConsultantSoldStorePackageAcceptRequest, \
    SoldStorePackage, SoldStoreUnpaidPackagePhase, SoldStorePaidPackagePhase, SoldStorePackagePhaseDetail
from .serializers import SoldStorePackagePhaseDetailPATCHSerializer, SoldStoreUnpaidPackagePhasePATCHSerializer
from ..consultants.models import ConsultantProfile
from .permissions import ConsultantSoldStorePackageAcceptRequestViewPermission, SoldStorePackageOwnerUpdatePermission, \
    SoldStorePackageGetPermission, SoldStorePackagePhaseGetPermission, SoldStorePackagePaidPhaseUpdatePermission, \
    SoldStorePackagePhaseDetailGetPermission, SoldStorePackagePhaseDetailUpdatePermission, \
    IsConsultantPutPostPermission, SoldStoreUnpaidPackagePhasePATCHPermission
from ...utils.custom.custom_permissions import IsConsultantPermission


class MarketplaceListAPIView(generics.ListAPIView):
    serializer_class = serializers.SoldStorePackageSerializer
    permission_classes = [permissions.IsAuthenticated, IsConsultantPermission]

    def get_queryset(self):
        consultant = ConsultantProfile.objects.get(user=self.request.user)
        accept_requested_store_packages_id_list = ConsultantSoldStorePackageAcceptRequest.objects.filter(
            consultant=consultant
        ).values_list("sold_store_package", flat=True)

        qs = SoldStorePackage.objects.filter(consultant=None).get_filled_student_detailed_infos().exclude(
            id__in=accept_requested_store_packages_id_list
        )
        return qs


class MarketplaceDetailAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = serializers.SoldStorePackageSerializer
    permission_classes = [permissions.IsAuthenticated, IsConsultantPermission]

    def get_queryset(self):
        qs = SoldStorePackage.objects.filter(consultant=None).get_filled_student_detailed_infos()
        return qs


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
    filterset_fields = ['sold_store_package']
    serializer_class = serializers.ConsultantSoldStorePackageAcceptRequestSerializer
    queryset = ConsultantSoldStorePackageAcceptRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated, ConsultantSoldStorePackageAcceptRequestViewPermission]


class ConsultantSoldStorePackageAcceptRequestListAPIView(generics.ListCreateAPIView):
    """
    Consultant in browsable API is ignored.
    """
    lookup_field = 'id'
    serializer_class = serializers.ConsultantSoldStorePackageAcceptRequestSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    filterset_fields = ['sold_store_package']

    def get_serializer_context(self):
        return {'request': self.request}

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

    def create(self, data, *args, **kwargs):
        # Here is changed
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        user = self.request.user

        try:
            data = request.data.copy()  # Default data is immutable
            consultant = ConsultantProfile.objects.get(user=user)
            data['consultant'] = consultant.id
            return self.create(data, *args, **kwargs)

        except ConsultantProfile.DoesNotExist:
            return Response({"detail": "User is not consultant."}, status=403)


class SoldStorePackageDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    Update format:
    {
        "consultant": 1
    }
    User can select consultant for sold store package.
    """
    lookup_field = 'id'
    serializer_class = serializers.SoldStorePackageSerializer
    queryset = SoldStorePackage.objects.all()
    permission_classes = [
        permissions.IsAuthenticated, SoldStorePackageOwnerUpdatePermission,
        SoldStorePackageGetPermission
    ]


class SoldStorePackageListAPIView(generics.ListAPIView):
    lookup_field = 'id'
    serializer_class = serializers.SoldStorePackageSerializer
    permission_classes = [permissions.IsAuthenticated, SoldStorePackageGetPermission]

    def get_queryset(self):
        user = self.request.user
        try:
            consultant = ConsultantProfile.objects.get(user=user)
            qs = SoldStorePackage.objects.filter(
                consultant=consultant
            )
        except ConsultantProfile.DoesNotExist:
            qs = SoldStorePackage.objects.filter(
                sold_to=user
            )
        return qs


class SoldStoreUnpaidPackagePhaseDetailAPIView(generics.RetrieveUpdateAPIView):
    http_method_names = ["options", "get", "patch"]
    lookup_field = 'id'
    queryset = SoldStoreUnpaidPackagePhase.objects.all()
    serializer_class = serializers.SoldStoreUnpaidPackagePhaseSerializer
    permission_classes = [
        permissions.IsAuthenticated, SoldStorePackagePhaseGetPermission,
        SoldStoreUnpaidPackagePhasePATCHPermission
    ]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PATCH':
            serializer_class = SoldStoreUnpaidPackagePhasePATCHSerializer

        return serializer_class


class SoldStoreUnpaidPackagePhaseListAPIView(generics.ListAPIView):
    lookup_field = 'id'
    serializer_class = serializers.SoldStoreUnpaidPackagePhaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['sold_store_package']

    def get_queryset(self):
        user = self.request.user

        try:
            consultant = ConsultantProfile.objects.get(user=user)
            qs = SoldStoreUnpaidPackagePhase.objects.filter(
                sold_store_package__consultant=consultant
            )
        except ConsultantProfile.DoesNotExist:
            qs = SoldStoreUnpaidPackagePhase.objects.filter(
                sold_store_package__sold_to=user
            )
        return qs


class SoldStorePaidPackagePhaseDetailAPIView(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = SoldStorePaidPackagePhase.objects.all()
    serializer_class = serializers.SoldStorePaidPackagePhaseSerializer
    permission_classes = [
        permissions.IsAuthenticated, SoldStorePackagePhaseGetPermission,
        SoldStorePackagePaidPhaseUpdatePermission
    ]


class SoldStorePaidPackagePhaseListAPIView(generics.ListAPIView):
    lookup_field = 'id'
    serializer_class = serializers.SoldStorePaidPackagePhaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['sold_store_package']

    def get_queryset(self):
        user = self.request.user

        try:
            consultant = ConsultantProfile.objects.get(user=user)
            qs = SoldStorePaidPackagePhase.objects.filter(
                sold_store_package__consultant=consultant
            )
        except ConsultantProfile.DoesNotExist:
            qs = SoldStorePaidPackagePhase.objects.filter(
                sold_store_package__sold_to=user
            )
        return qs


class SoldStorePackagePhaseDetailDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = SoldStorePackagePhaseDetail.objects.all()
    serializer_class = serializers.SoldStorePackagePhaseDetailSerializer
    permission_classes = [
        permissions.IsAuthenticated, SoldStorePackagePhaseDetailGetPermission,
        SoldStorePackagePhaseDetailUpdatePermission
    ]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PATCH':
            serializer_class = SoldStorePackagePhaseDetailPATCHSerializer

        return serializer_class


class SoldStorePackagePhaseDetailListAPIView(generics.ListCreateAPIView):
    lookup_field = 'id'
    serializer_class = serializers.SoldStorePackagePhaseDetailSerializer
    filter_class = SoldStorePackagePhaseDetailFilter
    permission_classes = [
        permissions.IsAuthenticated, IsConsultantPutPostPermission
    ]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        user = self.request.user
        is_consultant = ConsultantProfile.objects.filter(user=user).exists()

        if is_consultant:
            consultant = ConsultantProfile.objects.get(user=user)
            qs = SoldStorePackagePhaseDetail.objects.filter(
                Q(sold_store_unpaid_package_phase__sold_store_package__consultant=consultant) | Q(
                    sold_store_paid_package_phase__sold_store_package__consultant=consultant)
            )
        else:
            qs = SoldStorePackagePhaseDetail.objects.filter(
                Q(sold_store_unpaid_package_phase__sold_store_package__sold_to=user) | Q(
                    sold_store_paid_package_phase__sold_store_package__sold_to=user))
        return qs
