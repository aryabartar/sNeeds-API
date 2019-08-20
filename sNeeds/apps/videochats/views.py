from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils import timezone
from django.utils.timezone import now
from django.conf import settings

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from sNeeds.utils import skyroom
from sNeeds.apps.account.models import ConsultantProfile

from .models import Room
from .serializers import RoomSerializer
from .permissions import RoomOwnerPermission


class RoomListView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if ConsultantProfile.objects.filter(user=user).exists():
            qs = Room.objects.filter(sold_time_slot__consultant__user=user)
        else:
            qs = Room.objects.filter(sold_time_slot__sold_to=user)
        return qs


class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated, RoomOwnerPermission]
