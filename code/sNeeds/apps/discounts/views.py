from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CartConsultantDiscount, TimeSlotSaleNumberDiscount
from .serializers import CartConsultantDiscountSerializer, TimeSlotSaleNumberDiscountSerializer
from .permissions import CartConsultantDiscountPermission


class TimeSlotSaleNumberDiscountListView(generics.ListAPIView):
    queryset = TimeSlotSaleNumberDiscount.objects.all()
    serializer_class = TimeSlotSaleNumberDiscountSerializer
    permission_classes = []


class CartConsultantDiscountListView(generics.ListCreateAPIView):
    serializer_class = CartConsultantDiscountSerializer
    permission_classes = [CartConsultantDiscountPermission, permissions.IsAuthenticated]
    filterset_fields = ('cart',)

    def get_queryset(self):
        user = self.request.user
        qs = CartConsultantDiscount.objects.filter(cart__user=user)
        return qs


class CartConsultantDiscountDetailView(generics.RetrieveDestroyAPIView):
    queryset = CartConsultantDiscount.objects.all()
    serializer_class = CartConsultantDiscountSerializer
    permission_classes = [CartConsultantDiscountPermission, permissions.IsAuthenticated]
    lookup_field = 'id'
