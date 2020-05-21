from rest_framework import status, generics, mixins, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from .models import CartDiscount, TimeSlotSaleNumberDiscount, Discount
from .serializers import CartDiscountSerializer, TimeSlotSaleNumberDiscountSerializer, DiscountSerializer,\
    ConsultantInteractiveUsersSerializer
from .permissions import CartDiscountPermission, ConsultantPermission, ConsultantDiscountOwnersPermission
from sNeeds.apps.consultants.models import ConsultantProfile

User = get_user_model()


class TimeSlotSaleNumberDiscountListView(generics.ListAPIView):
    queryset = TimeSlotSaleNumberDiscount.objects.all()
    serializer_class = TimeSlotSaleNumberDiscountSerializer
    permission_classes = []


class CartDiscountListView(generics.ListCreateAPIView):
    serializer_class = CartDiscountSerializer
    permission_classes = [CartDiscountPermission, permissions.IsAuthenticatedOrReadOnly]
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
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConsultantForUserDiscountListCreateAPIView(generics.ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticated, ConsultantPermission]

    def get_queryset(self):
        user = self.request.user
        consultant_profile = ConsultantProfile.objects.get(user=user)
        qs = Discount.objects.filter(consultants=consultant_profile, creator='consultant')
        return qs


class ConsultantForUserDiscountRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticated, ConsultantPermission, ConsultantDiscountOwnersPermission]


class ConsultantInteractUserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ConsultantInteractiveUsersSerializer
    permission_classes = [permissions.IsAuthenticated, ConsultantPermission]

    def list(self, request, *args, **kwargs):
        from sNeeds.apps.consultants.models import ConsultantProfile
        user = None
        if request and hasattr(request, "user"):
            user = request.user
        consultant_profile = ConsultantProfile.objects.get(user=user)
        serializer = ConsultantInteractiveUsersSerializer(consultant_profile, context={'request': request})
        return Response(serializer.data)
