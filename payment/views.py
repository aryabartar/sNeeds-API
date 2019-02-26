from zeep import Client

from django.http import HttpResponse
from django.shortcuts import redirect

from rest_framework import generics, mixins, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from classes.models import PublicClass

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
        print(request.GET)
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')


class RequestPage(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_public_class(self, public_class_slug):
        public_class = PublicClass.objects.filter(slug__exact=public_class_slug)
        if public_class.exists():
            return public_class[0]
        return None

    def get(self, request, *args, **kwargs):
        # return send_request(request)
        return Response({})

    def post(self, request, *args, **kwargs):
        data = request.data
        if 'just_show' in data:
            if 'public_class' in data:
                public_class = self.get_public_class(data['public_class'])
                if public_class is not None:
                    if data['just_show'] == "true":
                        return Response({"title": public_class.title, "price": public_class.price})
                    else:
                        return send_request(request, amount=public_class.price)
                else:
                    return Response({"message": "No public_class found!"})

        return Response({"message": "Bad request format!"})
