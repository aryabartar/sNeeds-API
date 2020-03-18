from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CartDiscount, TimeSlotSaleNumberDiscount
from .serializers import CartDiscountSerializer, TimeSlotSaleNumberDiscountSerializer
from .permissions import CartDiscountPermission


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
