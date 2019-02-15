import random
import string

from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Discount, Cafe, UserDiscount
from .serializers import CafeSerializer, DiscountSerializer, UserDiscountSerializer
from account.permissions import CafeAdminAllowOnly


class CafeList(APIView):
    def get(self, request):
        all_cafes = Cafe.objects.all()
        serialize_cafe = CafeSerializer(all_cafes, many=True, context={'request': request})
        return Response(serialize_cafe.data)


class DiscountList(APIView):
    permission_classes = [CafeAdminAllowOnly]

    serializer_class = DiscountSerializer

    def post(self, request):
        discount_serializer = DiscountSerializer(data=request.data, context={"request": self.request})
        if discount_serializer.is_valid():
            discount_serializer.save()
            return Response(discount_serializer.data)
        else:
            return Response(discount_serializer.errors)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class UserDiscountList(mixins.CreateModelMixin,
                       generics.ListAPIView):
    serializer_class = UserDiscountSerializer
    passed_id = None

    def get_queryset(self):
        return UserDiscount.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CafePage(APIView):
    def get(self, request, cafe_pk):
        cafe = get_object_or_404(Cafe, pk=cafe_pk)
        cafe_serialize = CafeSerializer(cafe, context={'request': request})
        return Response(cafe_serialize.data)
