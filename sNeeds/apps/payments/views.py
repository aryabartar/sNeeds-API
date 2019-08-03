from zeep import Client

from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from sNeeds.apps.orders.models import Order

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
            request.build_absolute_uri(reverse("payment:verify")),
        )

        print(result)
        if result.Status == 100:
            return Response({"redirect": 'https://www.zarinpal.com/pg/StartPay/' + str(result.Authority)})
        else:
            return Response({"detail": 'Error code: ' + str(result.Status)}, 200)


def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], 100)
        print(result)
        if result.Status == 100:
            return JsonResponse({"detail": "Success", "ReflD": str(result.RefID)}, status=200)
        elif result.Status == 101:
            return JsonResponse({"detail": "Transaction submitted", "status": str(result.Status)}, status=200)
        else:
            return JsonResponse({"detail": "Transaction failed", "status": str(result.Status)}, status=400)
    else:
        return JsonResponse({"detail": "Transaction failed or canceled by user"}, status=400)


class TempVerify(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        order = Order.objects.filter(user=user, active=True, status="created")
