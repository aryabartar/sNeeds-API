import random
import string

from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Discount, Cafe, UserDiscount, UserUsedDiscount
from .serializers import CafeSerializer, DiscountSerializer, UserDiscountSerializer


class CafeList(APIView):
    def get(self, request):
        all_cafes = Cafe.objects.all()
        serialize_cafe = CafeSerializer(all_cafes, many=True, context={'request': request})
        return Response(serialize_cafe.data)


class DiscountDetail(APIView,
                     mixins.DestroyModelMixin):

    def get_object(self):
        discount_pk = self.kwargs['discount_pk']
        discount = get_object_or_404(Discount, pk=discount_pk)
        return discount

    def get(self, request, *args, **kwargs):
        discount_serialize = DiscountSerializer(self.get_object())
        return Response(discount_serialize.data)

    # TODO:Check bugs
    def delete(self, request, *args, **kwargs):
        discount = self.get_object()
        if request.user == discount.cafe.cafe_profile.user:
            return self.destroy(request, *args, **kwargs)
        return Response({"message": "You have to log in as cafe admin."})


class DiscountList(APIView):
    serializer_class = DiscountSerializer

    def get(self, request):
        all_discounts = Discount.objects.all()
        discounts_serialize = DiscountSerializer(all_discounts, many=True)
        return Response(discounts_serialize.data)

    def post(self, request):

        data = request.data
        # data['cafe'] = ['3']
        # print("\n\n\n\n\n\n")
        # print(data)
        # print("\n\n\n\n\n\n")
        discount_serializer = DiscountSerializer(data=data, context={"request": self.request})
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


class UserDiscountDetail(APIView,
                         mixins.DestroyModelMixin,
                         mixins.RetrieveModelMixin):
    serializer_class = UserDiscountSerializer

    def get_object(self):
        user_discount_pk = self.kwargs['user_discount_pk']
        user_discount = get_object_or_404(UserDiscount,
                                          pk=user_discount_pk)
        return user_discount

    def get_serializer(self, instance):
        serialize = self.serializer_class(instance)
        return serialize

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user_discount = self.get_object()
        if self.request.user == user_discount.user:
            return self.destroy(request, *args, **kwargs)
        return Response({"message": "Only user can delete its active discount. "})


class CafePage(APIView):
    def get(self, request, cafe_pk):
        cafe = get_object_or_404(Cafe, pk=cafe_pk)
        cafe_serialize = CafeSerializer(cafe, context={'request': request})
        return Response(cafe_serialize.data)
