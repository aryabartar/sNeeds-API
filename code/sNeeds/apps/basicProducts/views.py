from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import BasicProduct, SoldBasicProduct, ClassProduct, SoldClassProduct, WebinarProduct, SoldWebinarProduct
from .permissions import SoldBasicProductOwnerPermission


class BasicProductList(generics.ListAPIView):
    queryset = BasicProduct.objects.all()
    serializer_class = serializers.BasicProductSerializer


class BasicProductDetail(generics.RetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = serializers.BasicProductSerializer
    queryset = BasicProduct.objects.all()


class ClassProductList(generics.ListAPIView):
    queryset = ClassProduct.objects.all()
    serializer_class = serializers.ClassProductSerializer


class ClassProductDetail(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = ClassProduct.objects.all()
    serializer_class = serializers.ClassProductSerializer


class WebinarProductList(generics.ListAPIView):
    queryset = WebinarProduct.objects.all()
    serializer_class = serializers.WebinarProductSerializer


class WebinarProductDetail(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = WebinarProduct.objects.all()
    serializer_class = serializers.WebinarProductSerializer


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


class SoldClassProductList(generics.ListAPIView):
    queryset = SoldClassProduct.objects.all()
    serializer_class = serializers.SoldClassProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SoldClassProduct.objects.filter(sold_to=user)


class SoldClassProductDetail(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = SoldClassProduct.objects.all()
    serializer_class = serializers.SoldClassProductSerializer
    permission_classes = [IsAuthenticated, SoldBasicProductOwnerPermission]


class SoldWebinarProductList(generics.ListAPIView):
    queryset = SoldWebinarProduct.objects.all()
    serializer_class = serializers.SoldWebinarProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SoldWebinarProduct.objects.filter(sold_to=user)


class SoldWebinarProductDetail(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = SoldWebinarProduct.objects.all()
    serializer_class = serializers.SoldWebinarProductSerializer
    permission_classes = [IsAuthenticated, SoldBasicProductOwnerPermission]



