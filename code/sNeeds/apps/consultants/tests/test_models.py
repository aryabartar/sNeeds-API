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

class CartTests(CustomAPITestCase):
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
        # Setup ------
        self.client = APIClient()

    def test_consultant_profile_model_rate_correct(self):
        self.consultant1_profile.refresh_from_db()
        self.assertEqual(self.consultant1_profile.rate, 3.25)

        self.consultant2_profile.refresh_from_db()
        self.assertEqual(self.consultant2_profile.rate, None)
