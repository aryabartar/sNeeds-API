from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from . import models
from .permissions import OrderOwnerPermission


class OrderListView(generics.ListCreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        qs = models.Order.objects.filter(cart__user=user)
        return qs


class OrderDetailView(generics.RetrieveDestroyAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    lookup_field = 'id'
    permission_classes = (OrderOwnerPermission, permissions.IsAuthenticated)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.active and obj.status == "created":
            return self.destroy(request, *args, **kwargs)
        return Response({"detail": "Can not delete not active or paid order."})


# class OrderDetailAcceptView(APIView):
#
#     def post(self, request, *args, **kwargs):
#         order_id = kwargs.get('id', None)
#         order = models.Order.objects.get(id=order_id)
#