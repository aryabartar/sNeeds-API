from django.http import Http404

from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers

# class TimeSlotSailList(generics.GenericAPIView):

