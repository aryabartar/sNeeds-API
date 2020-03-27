import json
import time

from django.utils import timezone
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
from sNeeds.apps.store.serializers import SoldTimeSlotSaleSerializer
from sNeeds.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


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

        self.time_slot_sale_number_discount = TimeSlotSaleNumberDiscount.objects.create(
            number=2,
            discount=50
        )

    def test_sell_cart_create_order_working(self):
        #TODO: Update this later
        number_of_products = self.cart2.products.count()
        new_order = Order.objects.sell_cart_create_order(self.cart2)

        self.assertEqual(number_of_products, new_order.sold_products.count())
