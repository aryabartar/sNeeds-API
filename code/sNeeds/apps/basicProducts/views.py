from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import BasicProduct, SoldBasicProduct
from .permissions import SoldBasicProductOwnerPermission


class BasicProductList(generics.ListAPIView):
    queryset = BasicProduct.objects.all()
    serializer_class = serializers.BasicProductSerializer


class BasicProductDetail(generics.RetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = serializers.BasicProductSerializer
    queryset = BasicProduct.objects.all()


class SoldBasicProductList(generics.ListAPIView):
    queryset = SoldBasicProduct.objects.all()
    serializer_class = serializers.SoldBasicProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SoldBasicProduct.objects.filter(sold_to=user)


class SoldBasicProductDetail(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = serializers.SoldBasicProductSerializer
    queryset = SoldBasicProduct.objects.all()
    permission_classes = [IsAuthenticated, SoldBasicProductOwnerPermission]


