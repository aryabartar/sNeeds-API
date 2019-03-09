from django.shortcuts import render

from rest_framework import generics, mixins, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from cart.models import Cart
from .models import Order


class OrderDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart_obj, cart_created = Cart.objects.new_or_get(request)
        order = Order.objects.get_or_create(cart=cart_obj, user=request.user)
