from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import BugReportSerializer
from .models import BugReport


class BugReportCreateAPIView(generics.CreateAPIView):
    serializer_class = BugReportSerializer
    queryset = BugReport.objects.all()
