from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CartDiscount, TimeSlotSaleNumberDiscount, Discount
from .serializers import CartDiscountSerializer, TimeSlotSaleNumberDiscountSerializer, DiscountSerializer
from .permissions import CartDiscountPermission, ConsultantPermission
from sNeeds.apps.consultants.models import ConsultantProfile


class TimeSlotSaleNumberDiscountListView(generics.ListAPIView):
    queryset = TimeSlotSaleNumberDiscount.objects.all()
    serializer_class = TimeSlotSaleNumberDiscountSerializer
    permission_classes = []


class CartDiscountListView(generics.ListCreateAPIView):
    serializer_class = CartDiscountSerializer
    permission_classes = [CartDiscountPermission, permissions.IsAuthenticated]
    filterset_fields = ('cart',)

    def get_queryset(self):
        user = self.request.user
        qs = CartDiscount.objects.filter(cart__user=user)
        return qs


class CartDiscountDetailView(generics.RetrieveDestroyAPIView):
    queryset = CartDiscount.objects.all()
    serializer_class = CartDiscountSerializer
    permission_classes = [CartDiscountPermission, permissions.IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        discount = instance.dicount
        if discount.use_limit is not None:
            discount.use_limit = discount.use_limit + 1
        discount.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConsultantForUserDiscountListCreateAPIView(generics.ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticated, ConsultantPermission]

    def get_queryset(self):
        user = self.request.user
        consultant_profile = ConsultantProfile.objects.get(user=user)
        qs = Discount.objects.filter(consultants=consultant_profile, creator='C')
        return qs


class ConsultantForUserDiscountRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticated, ConsultantPermission]

    def get_queryset(self):
        user = self.request.user
        consultant_profile = ConsultantProfile.objects.get(user=user)
        qs = Discount.objects.filter(consultants=consultant_profile, creator='C')
        return qs
