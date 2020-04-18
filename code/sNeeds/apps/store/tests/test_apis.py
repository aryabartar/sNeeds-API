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
from sNeeds.apps.discounts.models import Discount, CartDiscount, TimeSlotSaleNumberDiscount
from sNeeds.apps.discounts.serializers import ShortDiscountSerializer
from sNeeds.apps.orders.models import Order
from sNeeds.apps.store.models import TimeSlotSale, SoldTimeSlotSale
from sNeeds.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


# from sNeeds.apps.carts.models import Cart

class StoreTests(CustomAPITestCase):
    def setUp(self):
        # Consultant discounts
        self.discount1 = Discount.objects.create(
            amount=10,
            code="discountcode1",
        )
        self.discount1.consultants.set([self.consultant1_profile, self.consultant2_profile])

        self.discount2 = Discount.objects.create(
            amount=20,
            code="discountcode2",
        )
        self.discount2.consultants.set([self.consultant1_profile, ])

        # Cart consultant discounts
        self.cart_discount1 = CartDiscount.objects.create(
            cart=self.cart1,
            discount=self.discount1
        )

        # Setup ------
        self.client = APIClient()

    def test_time_slot_sale_list_post_success(self):
        client = self.client
        client.login(email='c1@g.com', password='user1234')
        url = reverse("store:time-slot-sale-list")

        data = {
            "start_time": datetime.strftime(timezone.now() + timezone.timedelta(days=4), '%Y-%m-%dT%H:%M:%SZ')
        }
        response = client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        ts_obj = TimeSlotSale.objects.get(id=response.data.get("id"))
        self.assertEqual(
            response.data.get("start_time"),
            serializers.DateTimeField().to_representation(ts_obj.start_time)
        )
        self.assertEqual(
            response.data.get("end_time"),
            serializers.DateTimeField().to_representation(ts_obj.end_time)
        )
        self.assertEqual(response.data.get("price"), 100)
        self.assertEqual(response.data.get("consultant").get("id"), self.consultant1_profile.id)

    def test_time_slot_sale_list_post_fail(self):
        client = self.client
        client.login(email='c1@g.com', password='user1234')
        url = reverse("store:time-slot-sale-list")

        TimeSlotSale.objects.all().delete()

        data = {
            "start_time": datetime.strftime(timezone.now() + timezone.timedelta(minutes=50), '%Y-%m-%dT%H:%M:%SZ')
        }
        response = client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_time_slot_sale_detail_delete_success(self):
        client = self.client
        client.login(email='c1@g.com', password='user1234')

        ts_obj_id = TimeSlotSale.objects.filter(consultant=self.consultant1_profile).first().id

        url = reverse("store:time-slot-sale-detail", args=(ts_obj_id,))
        response = client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            TimeSlotSale.objects.filter(id=ts_obj_id).count(),
            0
        )

    def test_time_slot_sale_detail_delete_permission_fail(self):
        client = self.client
        client.login(email='c2@g.com', password='user1234')

        ts_obj_id = TimeSlotSale.objects.filter(consultant=self.consultant1_profile).first().id

        url = reverse("store:time-slot-sale-detail", args=(ts_obj_id,))
        response = client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            TimeSlotSale.objects.filter(id=ts_obj_id).count(),
            1
        )

    def test_sold_time_slot_sale_list_get_success(self):
        client = self.client
        client.login(email='c1@g.com', password='user1234')

        url = reverse("store:sold-time-slot-sale-list")
        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for sold_time_slot in response.data:
            self.assertEqual(sold_time_slot.get("consultant").get("id"), self.consultant1_profile.id)

    def test_sold_time_slot_sale_detail_get_permission_success(self):
        client = self.client
        client.login(email='c1@g.com', password='user1234')

        url = reverse("store:sold-time-slot-sale-detail", args=(self.sold_time_slot_sale1.id,))
        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sold_time_slot_sale_detail_get_permission_fail(self):
        client = self.client
        client.login(email='c2@g.com', password='user1234')

        url = reverse("store:sold-time-slot-sale-detail", args=(self.sold_time_slot_sale2.id,))
        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
