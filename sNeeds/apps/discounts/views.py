from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CartConsultantDiscount
from .serializers import CartConsultantDiscountSerializer
from .permissions import CartConsultantDiscountPermission

class CartConsultantDiscountListView(generics.ListCreateAPIView):
    queryset = CartConsultantDiscount.objects.all()
    serializer_class = CartConsultantDiscountSerializer


class CartConsultantDiscountDetailView(generics.RetrieveDestroyAPIView):
    queryset = CartConsultantDiscount.objects.all()
    serializer_class = CartConsultantDiscountSerializer
    permission_classes = [CartConsultantDiscountPermission,]
    lookup_field = 'id'
