from django.shortcuts import render
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from sNeeds.apps.customForms.models import BugReport
from PIL import Image
from rest_framework import generics
from .serializers import BugReportSerializer
from .models import BugReport


class SendBug(generics.CreateAPIView):
    serializer_class = BugReportSerializer
    queryset = BugReport.objects.all()


