from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Order, SoldOrder
from .permissions import OrderOwnerPermission, SoldOrderOwnerPermission


class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        qs = Order.objects.filter(cart__user=user)
        return qs


class OrderDetailView(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    lookup_field = 'id'
    permission_classes = (OrderOwnerPermission, permissions.IsAuthenticated)


class SoldOrderListView(generics.ListCreateAPIView):
    queryset = SoldOrder.objects.all()
    serializer_class = serializers.SoldOrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return SoldOrder.objects.filter(cart__user=self.request.user)


class SoldOrderDetailView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = SoldOrder.objects.all()
    serializer_class = serializers.SoldOrderSerializer
    permission_classes = (SoldOrderOwnerPermission, permissions.IsAuthenticated,)
