from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Cart, SoldCart
from .permissions import CartOwnerPermission, SoldCartOwnerPermission


class CartListView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = serializers.CartSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = serializers.CartSerializer
    lookup_field = 'id'
    permission_classes = (CartOwnerPermission, permissions.IsAuthenticated)


class SoldCartListView(generics.ListCreateAPIView):
    queryset = SoldCart.objects.all()
    serializer_class = serializers.SoldCartSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return SoldCart.objects.filter(user=self.request.user)


class SoldCartDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = SoldCart.objects.all()
    serializer_class = serializers.SoldCartSerializer
    permission_classes = (SoldCartOwnerPermission, permissions.IsAuthenticated)
