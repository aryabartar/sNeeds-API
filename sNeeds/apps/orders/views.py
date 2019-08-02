from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Order, SoldOrder
from .permissions import OrderOwnerPermission, SoldOrderOwnerPermission
from .tasks import create_random_user_accounts


class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        qs = Order.objects.filter(cart__user=user)
        create_random_user_accounts.delay()
        return qs


class OrderDetailView(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    lookup_field = 'id'
    permission_classes = (OrderOwnerPermission, permissions.IsAuthenticated)


class OrderDetailAcceptView(APIView):
    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('id', None)
        order = Order.objects.get(id=order_id)

        if order.total <= 0:
            return Response({"detail": "Cart is empty"}, 400)

        SoldOrder.objects.sell_order(order)
        return Response({"detail": "Sold order created"}, 201)


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
