from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from . import models
from .permissions import OrderOwnerPermission


class OrderListView(generics.ListCreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        qs = models.Order.objects.filter(billing_profile__user=user).exclude(status="created", active=False)
        return qs


class OrderDetailView(generics.RetrieveDestroyAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    lookup_field = 'id'
    permission_classes = (OrderOwnerPermission, permissions.IsAuthenticated)
