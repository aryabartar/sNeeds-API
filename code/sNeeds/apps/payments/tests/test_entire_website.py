import json

from django.utils import timezone
import time

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.datetime_safe import datetime
from rest_framework import status, serializers
from rest_framework.test import APITestCase, APIClient

from sNeeds.apps.account.models import Country, University, FieldOfStudy
from sNeeds.apps.carts.models import Cart
from sNeeds.apps.carts.serializers import CartSerializer
from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.discounts.models import ConsultantDiscount, CartConsultantDiscount, TimeSlotSaleNumberDiscount
from sNeeds.apps.discounts.serializers import ConsultantDiscountSerializer
from sNeeds.apps.orders.models import Order
from sNeeds.apps.store.models import TimeSlotSale, SoldTimeSlotSale
from sNeeds.apps.store.serializers import SoldTimeSlotSaleSerializer

User = get_user_model()


# from sNeeds.apps.carts.models import Cart

class CartTests(APITestCase):
    def setUp(self):
        self.SITE_URL = "http://127.0.0.1:8000/"
        self.client = APIClient()

    def test(self):
        client = self.client

        url = self.SITE_URL + "auth/accounts/"
        data = {
            "email": "u1@g.com",
            "password": "12345678",
            "phone_number": "09011353100"
        }
        r = client.post(url, data=data, format='json')
        token = r.data.get("token_response").get("token")
        client.credentials(Authorization= token)

        print(token)
        url = self.SITE_URL + "auth/my-account/"
        r = client.get(url, format='json')
        print(r.data)
