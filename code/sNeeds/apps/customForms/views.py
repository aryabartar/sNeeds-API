from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import BugReportSerializer, PackageFormSerializer
from .models import BugReport, PackageForm
from .permissions import PackageFormPermission


class BugReportCreateAPIView(generics.CreateAPIView):
    serializer_class = BugReportSerializer
    queryset = BugReport.objects.all()


class PackageFormListCreateAPIView(generics.ListCreateAPIView):
    queryset = PackageForm.objects.all()
    serializer_class = PackageFormSerializer
    permission_classes = (IsAuthenticated, PackageFormPermission)

    def get_queryset(self):
        user = self.request.user
        qs = PackageForm.objects.filter(user=user)
        return qs


class PackageFormRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = PackageForm.objects.all()
    serializer_class = PackageFormSerializer
    permission_classes = (IsAuthenticated, PackageFormPermission)

    def get_queryset(self):
        user = self.request.user
        qs = PackageForm.objects.filter(user=user)
        return qs



