import time
from celery.contrib.testing.worker import start_worker

from django.test import override_settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status, serializers
from rest_framework.test import APITestCase, APIClient

from sNeeds.apps.account.models import Country, University, FieldOfStudy
from sNeeds.apps.carts.models import Cart
from sNeeds.apps.carts.serializers import CartSerializer
from sNeeds.apps.comments.models import ConsultantComment, ConsultantAdminComment, SoldTimeSlotRate
from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.discounts.models import Discount, CartDiscount, TimeSlotSaleNumberDiscount
from sNeeds.apps.discounts.serializers import ShortDiscountSerializer
from sNeeds.apps.orders.models import Order
from sNeeds.apps.store.models import TimeSlotSale, SoldTimeSlotSale
from sNeeds.apps.store.tasks import delete_time_slots

from sNeeds.settings.celery.celery import app
from sNeeds.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


# from sNeeds.apps.carts.models import Cart
class CommentsTests(CustomAPITestCase):
    allow_database_queries = True

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

        self.consultant_comment1 = ConsultantComment.objects.create(
            user=self.user1,
            consultant=self.consultant1_profile,
            message="Message 1"
        )
        self.consultant_comment2 = ConsultantComment.objects.create(
            user=self.user1,
            consultant=self.consultant2_profile,
            message="Message 2"
        )
        self.consultant_comment3 = ConsultantComment.objects.create(
            user=self.user2,
            consultant=self.consultant2_profile,
            message="Message 3"
        )
        self.consultant_admin_comment1 = ConsultantAdminComment.objects.create(
            comment=self.consultant_comment1,
            message="Admin message 1"
        )
        self.consultant_admin_comment2 = ConsultantAdminComment.objects.create(
            comment=self.consultant_comment2,
            message="Admin message 2"
        )

        self.sold_time_slot_rate_1 = SoldTimeSlotRate.objects.create(
            sold_time_slot=self.sold_time_slot_sale1,
            rate=4
        )
        self.sold_time_slot_rate_2 = SoldTimeSlotRate.objects.create(
            sold_time_slot=self.sold_time_slot_sale2,
            rate=2.5
        )
        # Setup ------
        self.client = APIClient()

    def test_consultant_list_get_success(self):
        client = self.client
        url = reverse("comments:comment-list")

        response = client.get(url, format="json")

        self.assertEqual(len(response.data), len(ConsultantComment.objects.all()))

    def test_consultant_list_filter_user_get_success(self):
        client = self.client
        url = "%s?%s=%s" % (
            reverse("comments:comment-list"),
            "user",
            self.user1.id
        )

        response = client.get(url, format="json")

        self.assertEqual(len(response.data), 2)

    def test_consultant_list_filter_consultant_get_success(self):
        client = self.client
        url = "%s?%s=%s" % (
            reverse("comments:comment-list"),
            "consultant",
            self.consultant1_profile.id
        )

        response = client.get(url, format="json")

        self.assertEqual(len(response.data), 1)

    def test_consultant_list_post_success(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')
        url = reverse("comments:comment-list")

        consultant_comment_before_count = ConsultantComment.objects.all().count()
        data = {
            "consultant": self.consultant1_profile.id,
            "message": "hello"
        }
        response = client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ConsultantComment.objects.all().count(), consultant_comment_before_count + 1)
        self.assertEqual(response.data.get("user").get("id"), self.user1.id)

    def test_consultant_list_post_permission_fail(self):
        client = self.client
        url = reverse("comments:comment-list")

        data = {
            "consultant": self.consultant1_profile.id,
            "message": "hello"
        }
        response = client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_consultant_detail_get_success(self):
        client = self.client
        c1 = self.consultant_comment1

        url = reverse("comments:comment-detail", args=(c1.id,))
        response = client.get(url, format='json')
        data = response.data

        self.assertEqual(data.get("id"), c1.id)
        self.assertEqual(data.get("user").get("id"), c1.user.id)
        self.assertEqual(data.get("user").get("first_name"), c1.user.first_name)
        self.assertEqual(data.get("user").get("last_name"), c1.user.last_name)
        self.assertEqual(data.get("admin_reply"), "Admin message 1")
        self.assertEqual(data.get("consultant"), c1.consultant.id)
        self.assertEqual(data.get("message"), c1.message)
        self.assertEqual(data.get("created"), serializers.DateTimeField().to_representation(c1.created))
        self.assertEqual(data.get("updated"), serializers.DateTimeField().to_representation(c1.updated))

        url = reverse("comments:comment-detail", args=(self.consultant_comment3.id,))
        response = client.get(url, format='json')
        data = response.data

        self.assertEqual(data.get("admin_reply"), None)

    def test_sold_time_slot_rate_list_get_success(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        url = reverse("comments:sold-time-slot-rate-list")
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            SoldTimeSlotRate.objects.filter(sold_time_slot__sold_to=self.user1).count() + \
            SoldTimeSlotRate.objects.filter(sold_time_slot__consultant__user=self.user1).count()
        )

    def test_sold_time_slot_rate_get_filter_by_sold_time_slot_success(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')
        url = "%s?%s=%s" % (
            reverse("comments:sold-time-slot-rate-list"),
            "sold_time_slot",
            self.sold_time_slot_sale1.id
        )
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("sold_time_slot"), self.sold_time_slot_sale1.id)

    def test_sold_time_slot_rate_get_filter_by_sold_time_slot_fail(self):
        client = self.client
        url = "%s?%s=%s" % (
            reverse("comments:sold-time-slot-rate-list"),
            "sold_time_slot",
            self.sold_time_slot_sale3.id
        )
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sold_time_slot_rate_list_post_success(self):
        client = self.client
        client.login(email='u2@g.com', password='user1234')

        url = reverse("comments:sold-time-slot-rate-list")

        before_count = SoldTimeSlotRate.objects.all().count()
        data = {
            "sold_time_slot": self.sold_time_slot_sale3.id,
            "rate": 1
        }
        response = client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            before_count + 1,
            SoldTimeSlotRate.objects.all().count()
        )

    def test_sold_time_slot_rate_list_post_permission_denied(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        url = reverse("comments:sold-time-slot-rate-list")

        data = {
            "sold_time_slot": self.sold_time_slot_sale3.id,
            "rate": 1
        }
        response = client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
