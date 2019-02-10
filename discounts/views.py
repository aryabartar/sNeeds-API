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
    def get(self, requset):
        all_cafes = Cafe.objects.all()
        print("ss\n\n\n\n ;lskd ;lsak d;lksa ;dlk;salk")
        serialize_cafe = CafeSerializer(all_cafes, many=True)
        return Response(serialize_cafe.data)
