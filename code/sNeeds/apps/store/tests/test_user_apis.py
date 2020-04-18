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

class CartTests(CustomAPITestCase):
    def setUp(self):
        super().setUp()

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

    def test_time_slot_sales_list_get_success(self):
        client = self.client
        url = reverse("store:time-slot-sale-list")

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            TimeSlotSale.objects.all().count()
        )

    def test_time_slot_sales_list_get_consultant_query(self):
        client = self.client
        url = "%s?%s=%s" % (
            reverse("store:time-slot-sale-list"),
            "consultant",
            self.consultant2_profile.id
        )
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            TimeSlotSale.objects.filter(consultant=self.consultant2_profile).count()
        )

    def test_time_slot_sales_list_get_min_max_price(self):
        client = self.client
        url = "%s?%s=%s&%s=%s" % (
            reverse("store:time-slot-sale-list"),
            "price_min",
            100,
            "price_max",
            100
        )

        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            TimeSlotSale.objects.filter(price__lte=100, price__gte=100).count()
        )

        url = "%s?%s=%s&%s=%s" % (
            reverse("store:time-slot-sale-list"),
            "price_min",
            10,
            "price_max",
            1000
        )

        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            TimeSlotSale.objects.filter(price__lte=1000, price__gte=10).count()
        )

    def test_time_slot_sale_list_post_permission_denied(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        url = reverse("store:time-slot-sale-list")
        data = {
            "start-time": datetime.strftime(timezone.now() + timezone.timedelta(days=1), '%Y-%m-%dT%H:%M:%SZ')
        }
        response = client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_time_slot_sale_detail_get_success(self):
        client = self.client

        ts_obj = TimeSlotSale.objects.all().first()
        url = reverse("store:time-slot-sale-detail", args=(ts_obj.id,))

        response = client.get(url, format="json")

        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("id"), ts_obj.id)
        self.assertEqual(data.get("consultant").get("id"), ts_obj.consultant.id)
        self.assertEqual(
            data.get("start_time"),
            serializers.DateTimeField().to_representation(ts_obj.start_time)
        )
        self.assertEqual(
            data.get("end_time"),
            serializers.DateTimeField().to_representation(ts_obj.end_time)
        )
        self.assertEqual(
            data.get("price"),
            ts_obj.price
        )

    def test_time_slot_sale_detail_delete_permission_fail(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

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
        client.login(email='u1@g.com', password='user1234')

        url = reverse("store:sold-time-slot-sale-list")
        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for sold_time_slot in response.data:
            self.assertEqual(sold_time_slot.get("sold_to").get("id"), self.user1.id)

    def test_sold_time_slot_sale_list_get_unauthorized(self):
        client = self.client

        url = reverse("store:sold-time-slot-sale-list")
        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sold_time_slot_sale_list_get_consultant_filter(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        url = "%s?%s=%s" % (
            reverse("store:sold-time-slot-sale-list"),
            "consultant",
            self.consultant1_profile.id
        )
        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        url = "%s?%s=%s" % (
            reverse("store:sold-time-slot-sale-list"),
            "consultant",
            self.consultant2_profile.id
        )
        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_sold_time_slot_sale_detail_get_success(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        sts_obj = self.sold_time_slot_sale1
        url = reverse("store:sold-time-slot-sale-detail", args=(self.sold_time_slot_sale1.id,))

        response = client.get(url, format="json")
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("id"), sts_obj.id)
        self.assertEqual(data.get("consultant").get("id"), sts_obj.consultant.id)
        self.assertEqual(
            data.get("start_time"),
            serializers.DateTimeField().to_representation(sts_obj.start_time)
        )
        self.assertEqual(
            data.get("end_time"),
            serializers.DateTimeField().to_representation(sts_obj.end_time)
        )
        self.assertEqual(
            data.get("price"),
            sts_obj.price
        )
        self.assertEqual(data.get("sold_to").get("id"), sts_obj.sold_to.id)

    def test_sold_time_slot_sale_detail_get_permission_fail(self):
        client = self.client
        client.login(email='u2@g.com', password='user1234')

        url = reverse("store:sold-time-slot-sale-detail", args=(self.sold_time_slot_sale1.id,))
        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        client.logout()

        url = reverse("store:sold-time-slot-sale-detail", args=(self.sold_time_slot_sale1.id,))
        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sold_time_slot_sale_safe_detail_get_pass(self):
        client = self.client

        sts_obj = self.sold_time_slot_sale1

        url = reverse("store:sold-time-slot-sale-safe-detail", args=(self.sold_time_slot_sale1.id,))
        response = client.get(url, format="json")
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("id"), sts_obj.id)
        self.assertEqual(data.get("consultant").get("id"), sts_obj.consultant.id)
        self.assertEqual(
            data.get("start_time"),
            serializers.DateTimeField().to_representation(sts_obj.start_time)
        )
        self.assertEqual(
            data.get("end_time"),
            serializers.DateTimeField().to_representation(sts_obj.end_time)
        )
        self.assertEqual(
            data.get("price"),
            sts_obj.price
        )
        self.assertEqual(data.get("sold_to"), None)

    def test_sold_time_slot_sale_safe_list_get_pass(self):
        client = self.client

        url = reverse("store:sold-time-slot-sale-safe-list")
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), SoldTimeSlotSale.objects.all().count())
