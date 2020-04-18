import time
from celery.contrib.testing.worker import start_worker

from django.test import override_settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from sNeeds.apps.account.models import Country, University, FieldOfStudy
from sNeeds.apps.carts.models import Cart
from sNeeds.apps.carts.serializers import CartSerializer
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

        # Setup ------
        self.client = APIClient()

    def test_celery_task_delete_old_time_slot_sales(self):
        ts = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() - timezone.timedelta(minutes=1),
            end_time=timezone.now() + timezone.timedelta(minutes=1),
            price=self.consultant1_profile.time_slot_price
        )
        delete_time_slots()
        self.assertEqual(
            TimeSlotSale.objects.filter(id=ts.id).count(),
            0
        )
