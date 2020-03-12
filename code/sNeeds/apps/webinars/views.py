from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Webinar, SoldWebinar
from .persmissions import SoldWebinarOwnerPermission


class WebinarList(generics.ListAPIView):
    queryset = Webinar.objects.all()
    serializer_class = serializers.WebinarSerializer


class WebinarDetail(generics.RetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = serializers.WebinarSerializer
    queryset = Webinar.objects.all()


class SoldWebinarList(generics.ListAPIView):
    queryset = SoldWebinar.objects.all()
    serializer_class = serializers.SoldWebinarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SoldWebinar.objects.filter(sold_to=user)


class SoldWebinarDetail(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = serializers.SoldWebinarSerializer
    queryset = SoldWebinar.objects.all()
    permission_classes = [IsAuthenticated, SoldWebinarOwnerPermission]


