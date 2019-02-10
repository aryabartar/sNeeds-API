import random
import string

from rest_framework import generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from django.shortcuts import render, get_object_or_404
from .models import Discount, Cafe, UserDiscount
from .serializers import CafeSerializer


class CafeList(APIView):
    def get(self, request):
        all_cafes = Cafe.objects.all()
        serialize_cafe = CafeSerializer(all_cafes, many=True, context={'request': request})
        return Response(serialize_cafe.data)


class CafePage(APIView):
    def get(self, request, cafe_slug):
        cafe = Cafe.objects.get(slug__exact=cafe_slug)
        cafe_serialize = CafeSerializer(cafe, context={'request': request})
        return Response(cafe_serialize.data)
