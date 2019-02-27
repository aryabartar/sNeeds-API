import random
import string

from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Discount, Cafe, UserDiscount, UserDiscountArchive
from .serializers import (
    CafeSerializer,
    DiscountSerializer,
    UserDiscountSerializer,
    UserDiscountArchiveSerializer
)


class CafeList(APIView):
    def get(self, request):
        all_cafes = Cafe.objects.all()
        serialize_cafe = CafeSerializer(all_cafes, many=True, context={'request': request})
        return Response(serialize_cafe.data)


class DiscountDetail(APIView,
                     mixins.DestroyModelMixin):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        discount_pk = self.kwargs['discount_pk']
        discount = get_object_or_404(Discount, pk=discount_pk)
        return discount

    def get(self, request, *args, **kwargs):
        discount_serialize = DiscountSerializer(self.get_object())
        return Response(discount_serialize.data)

    def delete(self, request, *args, **kwargs):
        discount = self.get_object()
        if request.user == discount.cafe.cafe_profile.user:
            return self.destroy(request, *args, **kwargs)
        return Response({"message": "You have to log in as cafe admin."})


class DiscountList(APIView):
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        # print(request.session.get("a", "Unknown"))
        all_discounts = Discount.objects.all()
        discounts_serialize = DiscountSerializer(all_discounts, many=True)
        return Response(discounts_serialize.data)

    def post(self, request):
        data = request.data
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserDiscountSerializer
    passed_id = None

    def get_queryset(self):
        """Returns all UserDiscount objects for admin and UserDiscount of a certain cafe for a cafe admin."""
        user = self.request.user

        try:
            cafe_profile = user.cafe_profile
        except:
            cafe_profile = None

        if not user.is_authenticated:
            return None

        elif user.is_superuser:
            return UserDiscount.objects.all()

        elif cafe_profile is not None:
            cafe = cafe_profile.cafe
            user_discounts = UserDiscount.objects.filter(discount__cafe__exact=cafe)
            return user_discounts

        elif user.is_authenticated:
            return UserDiscount.objects.filter(user__exact=user)

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
        try:
            cafe_profile = user_discount.cafe
        except:
            pass
        if self.request.user == user_discount.user:  # Check permission
            return self.destroy(request, *args, **kwargs)
        return Response({"message": "Only user can delete its active discount. "})


class CafePage(APIView):
    def get(self, request, *args, **kwargs):
        cafe_slug = kwargs['cafe_slug']
        cafe = get_object_or_404(Cafe, slug=cafe_slug)
        cafe_serialize = CafeSerializer(cafe, context={'request': request})
        return Response(cafe_serialize.data)


class CafeDiscountsPage(APIView):
    def get(self, request, *args, **kwargs):
        cafe_slug = kwargs['cafe_slug']
        cafe = Cafe.objects.filter(slug__iexact=cafe_slug)
        if cafe.exists():
            discounts = cafe[0].discounts
            discounts_serialize = DiscountSerializer(discounts, many=True)
            return Response(discounts_serialize.data)
        return Response({"message": "No cafe found!"})


class UserDiscountArchiveList(generics.ListAPIView):
    serializer_class = UserDiscountArchiveSerializer

    def get_queryset(self):
        user = self.request.user

        try:
            cafe_profile = user.cafe_profile
        except:
            cafe_profile = None

        if not user.is_authenticated:
            return None

        elif cafe_profile is not None:
            cafe = cafe_profile.cafe
            user_discounts_archive = UserDiscountArchive.objects.filter(cafe__exact=cafe)
            return user_discounts_archive

        elif user.is_authenticated:
            return UserDiscountArchive.objects.filter(user__exact=user)

        return None
