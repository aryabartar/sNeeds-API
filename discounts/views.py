import random
import string
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from rest_framework import generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .models import Discount, Cafe, UserDiscount
from .serializers import CafeSerializer, DiscountSerializer, UserDiscountSerializer


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


class UserDiscountList(APIView):
    def post(self, request):
        data = request.data

        # Generates 5 digit random code
        discount_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)).lower()
        # To avoid same code generation
        while len(UserDiscount.objects.filter(code__exact=discount_code)) != 0:
            discount_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)).lower()

        data['code'] = discount_code
        user_discount_serializer = UserDiscountSerializer(data=data)

        if user_discount_serializer.is_valid():
            user_discount_serializer.save()
            return Response(user_discount_serializer.data)
        else:
            try:
                error_checker = user_discount_serializer.errors['non_field_errors']
                custom_error = {
                    'Developer Notes': 'If you are getting "The fields discount, user must make a unique set." error, '
                                       'Note that each user can only get one unique code on one discount. (No more than 1)'
                }
                errors = user_discount_serializer.errors
                errors['custom_error'] = custom_error

                return Response(errors)
            except:
                return Response(user_discount_serializer.errors)


class CafePage(APIView):

    def get(self, request, cafe_slug):
        cafe = Cafe.objects.get(slug__exact=cafe_slug)
        cafe_serialize = CafeSerializer(cafe, context={'request': request})
        return Response(cafe_serialize.data)
