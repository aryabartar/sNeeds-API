from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from . import models
from .permissions import CartOwnerPermission


class CartListView(generics.CreateAPIView):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CartDetailView(APIView):
    permission_classes = (CartOwnerPermission, permissions.IsAuthenticated)

    def get(self, request, *args, **kwargs):
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

    def put(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        qs = models.Cart.objects.filter(user=user)

        if not qs.exists():
            return Response({"detail": "No cart exists."}, 404)

        serializer = serializers.CartSerializer(qs.first(), data=data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)

        return Response(serializer.errors, 400)
