from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse
from django.shortcuts import redirect

from zeep import Client

from .permissions import OrderOwnerPermission
from sNeeds.apps.orders.models import Order

MERCHANT = 'd40321dc-8bb0-11e7-b63c-005056a205be'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')


def is_authenticated(user):
    if not user:
        return False
    if user.is_authenticated:
        return True
    return False


class SendRequest(APIView):
    permission_classes = [OrderOwnerPermission, ]

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        if not is_authenticated(user):
            return Response({"detail": "User is not authenticated"}, 401)

        order_id = data.get('order', None)
        if not order_id:
            return Response({"detail": "Order_id is empty"}, 400)

        order_qs = Order.objects.filter(id=order_id)
        if order.count() != 1:
            return Response({"detail": "No order exists"}, 400)

        order = order_qs.first()
        if order.status != "created":
            return Response({"detail": "This order is not ready for payment (check status)"}, 400)
        if not order.active:
            return Response({"detail": "Order is not active"}, 400)

        if not self.check_object_permissions(request, order):
            return Response({"detail": "Order is not for this user"}, 400)

        if order.total <= 0:
            return Response({"detail": "Order is empty"}, 400)

        result = client.service.PaymentRequest(
            MERCHANT,
            100,
            "پرداخت اسنیدز",
            order.billing_profile.user.email,
            order.billing_profile.user.phone_number,
            'http://localhost:8000/payment/verify/'
        )

        if result.Status == 100:
            return Response({"redirect": 'https://www.zarinpal.com/pg/StartPay/' + str(result.Authority)})
        else:
            return Response({"detail": 'Error code: ' + str(result.Status)}, 200)


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
