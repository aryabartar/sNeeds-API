from zeep import Client

from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect

from django.conf import settings

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from sNeeds.apps.orders.models import Order

from .models import PayPayment
from ..carts.models import Cart

ZARINPAL_MERCHANT = settings.ZARINPAL_MERCHANT


class SendRequest(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')

        user = request.user

        try:
            cart_id = kwargs.get("cartid")
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            return Response({"detail": "No cart exists."}, 400)

        if not cart.user == user:
            return Response({"detail": "This user is not cart's owner."}, 400)

        # TODO: Change for 100% discounts.
        if not cart.is_acceptable_for_pay():
            return Response({"detail": "Can not pay, The price is 0."}, 400)

        result = client.service.PaymentRequest(
            ZARINPAL_MERCHANT,
            int(cart.total),
            "پرداخت اسنیدز",
            cart.user.email,
            cart.user.phone_number,
            "http://37.152.182.253/payment/accept/",
        )

        if result.Status != 100:
            return Response({"detail": 'Error code: ' + str(result.Status)}, 400)

        PayPayment.objects.create(user=user, cart=cart, authority=result.Authority)

        return Response({"redirect": 'https://www.zarinpal.com/pg/StartPay/' + str(result.Authority)})


class Verify(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')

        data = request.data
        print(data)
        if data.get('status') == 'OK':
            user = request.user
            authority = data.get('authority', None)

            try:
                payment = PayPayment.objects.get(
                    user=user,
                    authority=authority
                )

            except PayPayment.DoesNotExist:
                return Response({"detail": "PayPayment does not exists."}, status=400)

            result = client.service.PaymentVerification(ZARINPAL_MERCHANT, authority, int(payment.cart.total))

            if result.Status == 100:
                Order.objects.sell_cart_create_order(payment.cart)
                return Response({"detail": "Success", "ReflD": str(result.RefID)}, status=200)
            elif result.Status == 101:
                return Response({"detail": "Transaction submitted", "status": str(result.Status)}, status=200)
            else:
                return Response({"detail": "Transaction failed", "status": str(result.Status)}, status=400)

        else:
            return Response({"detail": "Transaction failed or canceled by user"}, status=400)


class VerifyTest(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        cart_id = request.query_params.get("id")
        Order.objects.sell_cart_create_order(Cart.objects.get(id=cart_id))
        return HttpResponse()
