import random
import string

from django.shortcuts import render, get_object_or_404
from .models import Discount, Cafe, UserDiscount

from rest_framework import generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


class CafeList(APIView):
    def get(self):
        all_cafes = Cafe.objects.all()
