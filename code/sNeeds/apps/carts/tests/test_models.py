import json

from django.core.exceptions import ValidationError
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from sNeeds.apps.account.models import Country, University, FieldOfStudy
from sNeeds.apps.carts.models import Cart
from sNeeds.apps.carts.serializers import CartSerializer
from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.store.models import TimeSlotSale
from sNeeds.apps.store.serializers import TimeSlotSaleSerializer
from sNeeds.apps.storePackages.serializers import StorePackageSerializer
from sNeeds.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


class CartModelTests(CustomAPITestCase):
    def setUp(self):
        super().setUp()

    def test_cart_create_user_is_consultant_fail(self):
        with self.assertRaises(ValidationError) as e:
            Cart.objects.create(user=self.consultant1)

    def test_change_product_to_inactive_remove_from_products_total_subtotal_correct_without_discount(self):
        cart = self.cart4
        products = self.cart4.products.all()

        subtotal = 0
        for p in products:
            subtotal += p.price

        total = subtotal

        self.assertEqual(cart.subtotal, subtotal)
        self.assertEqual(cart.total, total)

        self.store_package_1.active = False
        self.store_package_1.save()

        self.cart4.refresh_from_db()
        cart = self.cart4

        products = cart.products.all()

        subtotal2 = 0
        for p in products:
            subtotal2 += p.price
        total2 = subtotal2

        print(total)
        print(self.store_package_1.price)
        print(total2)

        self.assertEqual(cart.subtotal, subtotal2)
        self.assertEqual(cart.total, total2)
        self.assertEqual(total2, total - self.store_package_1.price)
