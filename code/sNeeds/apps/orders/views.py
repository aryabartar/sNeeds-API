from rest_framework import status, generics, mixins, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Order
from .permissions import OrderOwnerPermission


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created', ]

    def get_queryset(self):
        user = self.request.user
        qs = Order.objects.filter(user=user)
        return qs


class OrderDetailView(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    lookup_field = 'id'
    permission_classes = (OrderOwnerPermission, permissions.IsAuthenticated)
