from zeep import Client

from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PayPayment

from sNeeds.apps.orders.models import Order, SoldOrder

MERCHANT = 'd40321dc-8bb0-11e7-b63c-005056a205be'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')


class SendRequest(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        user = request.user

        try:
            order = Order.objects.get(cart__user=user)
        except Order.DoesNotExist:
            return Response({"detail": "User has no order"}, 400)

        if not order.is_acceptable_for_pay():
            return Response({"detail": "Can not pay this order"}, 400)

        result = client.service.PaymentRequest(
            MERCHANT,
            int(order.total),
            "پرداخت اسنیدز",
            order.cart.user.email,
            order.cart.user.phone_number,
            "http://193.176.241.131:8080/payment/accept/",
        )

        PayPayment.objects.get_or_create(user=user, order=order, authority=result.Authority)

        if result.Status == 100:
            return Response({"redirect": 'https://www.zarinpal.com/pg/StartPay/' + str(result.Authority)})

        else:
            return Response({"detail": 'Error code: ' + str(result.Status)}, 200)


class Verify(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        data = request.data
        if data.get('status', None) == 'OK':
            user = request.user

            try:
                payment = PayPayment.objects.get(user=user)
            except PayPayment.DoesNotExist:
                return Response({"detail": "Payment error"}, status=400)

            result = client.service.PaymentVerification(MERCHANT, data.get('authority', None), int(payment.order.total))
            payment.delete()

            if result.Status == 100:
                SoldOrder.objects.sell_order(payment.order)
                return Response({"detail": "Success", "ReflD": str(result.RefID)}, status=200)
            elif result.Status == 101:
                return Response({"detail": "Transaction submitted", "status": str(result.Status)}, status=200)
            else:
                return Response({"detail": "Transaction failed", "status": str(result.Status)}, status=400)

        else:
            return Response({"detail": "Transaction failed or canceled by user"}, status=400)
