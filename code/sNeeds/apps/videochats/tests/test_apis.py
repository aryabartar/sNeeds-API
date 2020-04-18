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
from sNeeds.apps.videochats.models import Room
from sNeeds.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


class VideoChatTests(CustomAPITestCase):
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
        self.sold_time_slot_sale1 = SoldTimeSlotSale.objects.create(
            sold_to=self.user1,
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(days=2),
            end_time=timezone.now() + timezone.timedelta(days=2, hours=1),
            price=self.consultant1_profile.time_slot_price
        )

        self.sold_time_slot_sale2 = SoldTimeSlotSale.objects.create(
            sold_to=self.user2,
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(days=2, hours=1),
            end_time=timezone.now() + timezone.timedelta(days=2, hours=2),
            price=self.consultant1_profile.time_slot_price
        )

        self.sold_time_slot_sale3 = SoldTimeSlotSale.objects.create(
            sold_to=self.user2,
            consultant=self.consultant2_profile,
            start_time=timezone.now() + timezone.timedelta(days=2),
            end_time=timezone.now() + timezone.timedelta(days=2, hours=1),
            price=self.consultant2_profile.time_slot_price
        )

        self.sold_time_slot_rate_1 = SoldTimeSlotRate.objects.create(
            sold_time_slot=self.sold_time_slot_sale1,
            rate=4
        )
        self.sold_time_slot_rate_2 = SoldTimeSlotRate.objects.create(
            sold_time_slot=self.sold_time_slot_sale2,
            rate=2.5
        )

        self.room1 = Room.objects.create(
            sold_time_slot=self.sold_time_slot_sale1,
        )
        self.room2 = Room.objects.create(
            sold_time_slot=self.sold_time_slot_sale2
        )

        # Setup ------
        self.client = APIClient()

    def test_rooms_list_get_success(self):
        client = self.client
        url = reverse("videochat:room-list")

        client.login(email="u1@g.com", password="user1234")
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            1
        )

        client.login(email="u2@g.com", password="user1234")
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            1
        )

        client.login(email="c1@g.com", password="user1234")
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            2
        )

        Room.objects.create(
            sold_time_slot=self.sold_time_slot_sale3
        )
        client.login(email="u2@g.com", password="user1234")
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            2
        )

        Room.objects.all().delete()
        client.login(email="u1@g.com", password="user1234")
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            0
        )

    def test_rooms_list_get_filter_by_sold_time_slot(self):
        client = self.client
        client.login(email="u1@g.com", password="user1234")

        url = "%s?%s=%s" % (
            reverse("videochat:room-list"),
            "sold_time_slot",
            self.sold_time_slot_sale1.id
        )
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("sold_time_slot"), self.sold_time_slot_sale1.id)

        url = "%s?%s=%s" % (
            reverse("videochat:room-list"),
            "sold_time_slot",
            self.sold_time_slot_sale3.id
        )
        response = client.get(url, format='json')

        # TODO: This should be HTTP_403
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_rooms_list_authenticate_permission(self):
        client = self.client
        url = reverse("videochat:room-list")

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_rooms_detail_get_success(self):
        client = self.client
        url = reverse("videochat:room-detail", args=(self.room1.id,))

        self.room1.room_id = 10
        self.room1.user_id = 11
        self.room1.consultant_id = 12
        self.room1.user_login_url = "http://127.0.0.1:8000/"
        self.room1.consultant_login_url = "http://127.0.0.1:8000/c"
        self.room1.save()
        self.room1.refresh_from_db()

        # For user
        client.login(email="u1@g.com", password="user1234")
        response = client.get(url, format='json')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("id"), self.room1.id)
        self.assertEqual(data.get("sold_time_slot"), self.room1.sold_time_slot.id)
        self.assertEqual(data.get("login_url"), self.room1.user_login_url)
        self.assertEqual(
            data.get("start_time"),
            self.room1.sold_time_slot.start_time
        )
        self.assertEqual(
            data.get("end_time"),
            self.room1.sold_time_slot.end_time
        )

        # For consultant
        client.login(email="c1@g.com", password="user1234")
        response = client.get(url, format='json')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("id"), self.room1.id)
        self.assertEqual(data.get("sold_time_slot"), self.room1.sold_time_slot.id)
        self.assertEqual(data.get("login_url"), self.room1.consultant_login_url)
        self.assertEqual(
            data.get("start_time"),
            self.room1.sold_time_slot.start_time
        )
        self.assertEqual(
            data.get("end_time"),
            self.room1.sold_time_slot.end_time
        )

    def test_rooms_detail_get_permission_denied(self):
        client = self.client
        url = reverse("videochat:room-detail", args=(self.room1.id,))

        # For user
        client.login(email="u2@g.com", password="user1234")
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rooms_detail_get_unauthorized(self):
        client = self.client
        url = reverse("videochat:room-detail", args=(self.room1.id,))

        # For user
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
