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


class OrderTests(CustomAPITestCase):
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
        number_of_products = self.cart2.products.count()
        new_order = Order.objects.sell_cart_create_order(self.cart2)

        self.assertFalse(Cart.objects.filter(pk=self.cart2.id).exists())
        self.assertEqual(self.cart2.subtotal, new_order.subtotal)
        self.assertEqual(self.cart2.total, new_order.total)
        self.assertEqual(number_of_products, new_order.sold_products.count())

    def test_order_id_creation_correct(self):
        new_order = Order.objects.sell_cart_create_order(self.cart2)
        self.assertIsNotNone(new_order.order_id)
        self.assertEqual(Order.objects.filter(order_id=new_order.order_id).count(), 1)

    def test_time_slots_remove_from_other_carts_create_order(self):
        cart1 = Cart.objects.create(user=self.user1)
        cart1.products.set([self.time_slot_sale1])

        cart2 = Cart.objects.create(user=self.user2)
        cart2.products.set([self.time_slot_sale1, self.time_slot_sale5])

        order = Order.objects.sell_cart_create_order(cart=cart1)

        cart2.refresh_from_db()

        self.assertEqual(cart2.products.all().count(), 1)
        self.assertEqual(cart2.products.all().first().id, self.time_slot_sale5.id)
