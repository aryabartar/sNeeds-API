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


class DiscountDetail(APIView):
    def get(self, request, discount_pk):
        discount = get_object_or_404(Discount, pk=discount_pk)
        discount_serialize = DiscountSerializer(discount)
        return Response(discount_serialize.data)


class DiscountList(APIView):
    serializer_class = DiscountSerializer

    def get(self, request):
        all_discounts = Discount.objects.all()
        discounts_serialize = DiscountSerializer(all_discounts, many=True)
        return Response(discounts_serialize.data)

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
        """Returns all UserDiscount objects for admin and UserDiscount of a certain cafe for a cafe admin."""
        user = self.request.user

        if not user.is_authenticated:
            return None
        elif user.is_superuser:
            return UserDiscount.objects.all()
        elif user.cafe_profile is not None:
            cafe = user.cafe_profile.cafe
            user_discounts = UserDiscount.objects.filter(discount__cafe__exact=cafe)
            return user_discounts

        return None

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Unique code validation"""
        qs = UserDiscount.objects.filter(user__exact=request.user, discount__pk__exact=request.data['discount'])
        if qs.exists():
            return Response({"message": "This user already has an active code."})
        return self.create(request, *args, **kwargs)


class UserDiscountDetail(generics.GenericAPIView,
                         mixins.DestroyModelMixin):

    def get_queryset(self):
        print("ss")
        print(self.request)
        return UserDiscount.objects.first()

    def destroy(self, request, *args, **kwargs):
        return self.destroy(request , *args , **kwargs)

    def get(self, request, *args, **kwargs):
        return Response({"s":"S"})

class CafePage(APIView):
    def get(self, request, cafe_pk):
        cafe = get_object_or_404(Cafe, pk=cafe_pk)
        cafe_serialize = CafeSerializer(cafe, context={'request': request})
        return Response(cafe_serialize.data)
