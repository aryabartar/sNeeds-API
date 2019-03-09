from zeep import Client

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

from rest_framework import generics, mixins, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from classes.models import PublicClass
from order.models import Order
from .models import Cart

from order.serializers import OrderSerializer
from .serializers import CartSerializer

MERCHANT = 'd40321dc-8bb0-11e7-b63c-005056a205be'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09011353909'  # Optional
CallbackURL = 'http://127.0.0.1:8000/payment/verify/'  # Important: need to edit for realy server.


def send_request(request, amount):
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return Response({'Error code: ', str(result.Status)})


def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')


class CartHome(APIView):
    def get(self, request, *args, **kwargs):
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cart_serialize = CartSerializer(cart_obj)
        return Response(cart_serialize.data)


class CartUpdate(APIView):
    permission_classes = [permissions.AllowAny]

    def get_boolean_from_string_or_none(self, str):
        if str == "true":
            str = True
        elif str == "false":
            str = False
        else:
            str = None
        return str

    def put(self, request, *args, **kwargs):
        public_class_slug = request.data.get("public_class_slug", None)
        add_to_cart = self.get_boolean_from_string_or_none(request.data.get("add_to_cart", None))

        if public_class_slug is not None and add_to_cart is not None:

            try:
                public_class_obj = PublicClass.objects.get(slug=public_class_slug)
            except PublicClass.DoesNotExist:
                return Response({"message": "No product found."})

            cart_obj, new_obj = Cart.objects.new_or_get(request)

            if add_to_cart is True:
                cart_obj.public_classes.add(public_class_obj)
            else:
                cart_obj.public_classes.remove(public_class_obj)

            return Response({"status": "OK"})

        else:
            return Response({"message": "Bad request."})


class OrderHome(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart_obj, cart_created = Cart.objects.new_or_get(request)
        order, order_created = Order.objects.get_or_create(cart=cart_obj, user=request.user)
        order_serialize = OrderSerializer(order)
        return Response(order_serialize.data)
