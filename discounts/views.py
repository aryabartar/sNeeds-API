import random
import string
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from rest_framework import generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .models import Discount, Cafe, UserDiscount
from .serializers import CafeSerializer, DiscountSerializer


class CafeList(APIView):
    def get(self, request):
        all_cafes = Cafe.objects.all()
        serialize_cafe = CafeSerializer(all_cafes, many=True, context={'request': request})
        return Response(serialize_cafe.data)


class DiscountList(APIView):
    serializer_class = DiscountSerializer

    def post(self, request):
        discount_serializer = DiscountSerializer(data=request.data)
        if discount_serializer.is_valid():
            discount_serializer.save()
            return Response(discount_serializer.data)
        else:
            return Response(discount_serializer.errors)


class CafePage(APIView):

    def get(self, request, cafe_slug):
        cafe = Cafe.objects.get(slug__exact=cafe_slug)
        cafe_serialize = CafeSerializer(cafe, context={'request': request})
        return Response(cafe_serialize.data)
