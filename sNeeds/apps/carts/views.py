from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from . import models
from .permissions import CartOwnerPermission


class CartListView(APIView):
    """
    POST:
    {
        "time_slot_sales" : [10,11]
    }
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        data.update({"user": request.user.pk})
        serializer = serializers.CartSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        return Response(serializer.errors, 400)


class CartDetailView(APIView):
    permission_classes = (CartOwnerPermission, permissions.IsAuthenticated)

    def get(self, request, *args, **kwargs):
        print()
        if request.user.id != kwargs.get('id', None):
            return Response({"detail": "You are not logged in as this user."}, 403)

        qs = models.Cart.objects.filter(user=self.request.user)
        if qs.exists():
            cart_obj = qs.first()
            self.check_object_permissions(request, cart_obj)
            serializer = serializers.CartSerializer(cart_obj)
            return Response(serializer.data, 200)
        else:
            return Response({"detail": "Not found."}, 404)
