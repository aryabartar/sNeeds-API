from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Cart
from .permissions import CartOwnerPermission


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

