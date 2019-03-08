from zeep import Client

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

from rest_framework import generics, mixins, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from classes.models import PublicClass
from .models import Cart

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
        cart_obj, cart_new_obj = Cart.objects.new_or_get(request)
        public_classes = cart_obj.public_classes.all()
        total = 0
        for public_class in public_classes:
            total += public_class.price
        cart_obj.total = total
        cart_obj.save()
        return Response({"GET": "GET"})


class CartUpdate(APIView):
    def put(self, request, *args, **kwargs):
        public_class_slug = request.data.get("public_class_slug", None)
        add_to_cart = request.data.get("add_to_cart", None)

        if add_to_cart == "true":
            add_to_cart = True
        elif add_to_cart == "false":
            add_to_cart = False
        else:
            add_to_cart = None

        if public_class_slug is not None and add_to_cart is not None:
            public_class_qs = PublicClass.objects.filter(slug=public_class_slug)

            if public_class_qs.exists():
                public_class_obj = public_class_qs[0]
                cart_obj, new_obj = Cart.objects.new_or_get(request)

                if add_to_cart is True:
                    print("true")
                    cart_obj.public_classes.add(public_class_obj)
                else:
                    print("running this")
                    cart_obj.public_classes.remove(public_class_obj)

                return Response({"status": "OK"})

            else:
                return Response({"message": "No product found."})

        else:
            return Response({"message": "Bad request."})
