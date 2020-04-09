import json

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


class CartTests(CustomAPITestCase):
    def setUp(self):
        super().setUp()

    def test_cart_list_get_success(self):
        url = reverse("cart:cart-list")
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        response = client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for item in response.data:
            self.assertEqual(item.get("user"), self.user1.id)

        self.assertEqual(len(response.data), Cart.objects.filter(user=self.user1).count())

    def test_cart_list_post_success(self):
        url = reverse("cart:cart-list")
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        products = [self.time_slot_sale1, self.time_slot_sale2, self.time_slot_sale5, self.store_package_1]
        data = {"products": [i.id for i in products], }
        response = client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            [i.id for i in products].sort(),
            [response.data.get("products")].sort()
        )

    def test_post_cart_not_pass_time_conflict(self):
        url = reverse("cart:cart-list")
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        # Test 1
        products = [self.time_slot_sale1, self.time_slot_sale2, self.time_slot_sale4]
        data = {"products": [i.id for i in products]}
        response = client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test 2
        self.temp_time_slot_sale = TimeSlotSale.objects.create(
            consultant=self.consultant2_profile,
            start_time=timezone.now() + timezone.timedelta(hours=2, minutes=2),
            end_time=timezone.now() + timezone.timedelta(hours=2, minutes=10),
            price=self.consultant2_profile.time_slot_price
        )
        products = [self.time_slot_sale2, self.temp_time_slot_sale]
        data = {"products": [i.id for i in products]}
        response = client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.temp_time_slot_sale.delete()

        # Test 3
        self.temp_time_slot_sale = TimeSlotSale.objects.create(
            consultant=self.consultant2_profile,
            start_time=timezone.now() + timezone.timedelta(hours=2, minutes=5),
            end_time=timezone.now() + timezone.timedelta(hours=3, minutes=5),
            price=self.consultant2_profile.time_slot_price
        )
        products = [self.time_slot_sale2, self.temp_time_slot_sale]
        data = {"products": [i.id for i in products]}
        response = client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.temp_time_slot_sale.delete()

        # Test 4
        self.temp_time_slot_sale = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(hours=6, minutes=50),
            end_time=timezone.now() + timezone.timedelta(hours=7, minutes=50),
            price=self.consultant1_profile.time_slot_price
        )
        products = [self.time_slot_sale5, self.temp_time_slot_sale]
        data = {"products": [i.id for i in products]}
        response = client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.temp_time_slot_sale.delete()

    def test_get_cart_authorization(self):
        url = reverse("cart:cart-list")
        client = self.client
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_cart_authorization(self):
        url = reverse("cart:cart-list")
        client = self.client
        response = client.post(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cart_price_validity(self):
        url = reverse("cart:cart-list")
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        products = [self.time_slot_sale1, self.time_slot_sale2, self.time_slot_sale5, self.store_package_1]
        data = {"products": [i.id for i in products], }
        response = client.post(url, data=data, format='json')

        expected_price = 0
        for t in products:
            expected_price += t.price

        # After creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("total"), expected_price)
        self.assertEqual(response.data.get("subtotal"), expected_price)

        # After deleting one product
        new_cart_id = response.data.get("id")
        url = reverse("cart:cart-detail", args=(new_cart_id,))
        deleted_product = products.pop(0)
        expected_price -= deleted_product.price
        deleted_product.delete()
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("total"), expected_price)
        self.assertEqual(response.data.get("subtotal"), expected_price)

    def test_empty_cart_creation_error(self):
        url = reverse("cart:cart-list")
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        data = {"products": [], }
        response = client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_other_user_cart_access_denied(self):
        cart = self.cart3
        url = reverse("cart:cart-detail", args=(cart.id,))
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_cart_detail(self):
        cart = self.cart2
        url = reverse("cart:cart-detail", args=(cart.id,))
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cart.total, response.data.get("total"))
        self.assertEqual(cart.subtotal, response.data.get("subtotal"))

        self.assertEqual(
            TimeSlotSaleSerializer(
                cart.products.all().get_time_slot_sales(),
                context={"request": response.wsgi_request},
                many=True
            ).data,
            response.data.get("time_slot_sales")
        )

        self.assertEqual(
            StorePackageSerializer(
                cart.products.all().get_store_packages(),
                context={"request": response.wsgi_request},
                many=True
            ).data,
            response.data.get("store_packages")
        )

    def test_remove_product_from_cart_updates_price(self):
        self.assertEqual(
            self.cart1.total,
            self.time_slot_sale1.price + self.time_slot_sale2.price
        )
        self.cart1.products.remove(self.time_slot_sale1)
        self.assertEqual(
            self.cart1.total,
            self.time_slot_sale2.price
        )

    def test_consultant_can_not_create_cart(self):
        url = reverse("cart:cart-list")
        client = self.client
        client.force_login(self.consultant1)
        products = [self.time_slot_sale1, self.time_slot_sale2, self.time_slot_sale5, self.store_package_1]
        data = {"products": [i.id for i in products], }
        response = client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_cart_with_inactive_product_fails(self):
        url = reverse("cart:cart-list")
        client = self.client
        client.force_login(self.user1)
        self.store_package_1.active = False
        self.store_package_1.save()

        products = [self.time_slot_sale1, self.time_slot_sale2, self.time_slot_sale5, self.store_package_1]
        data = {"products": [i.id for i in products], }
        response = client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_delete_cart_fails(self):
        url = reverse("cart:cart-list")
        client = self.client
        client.force_login(self.user1)

        products = [self.time_slot_sale1, self.time_slot_sale2, self.time_slot_sale5, self.store_package_1]
        data = {"products": [i.id for i in products], }

        response = client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # print(response.data)

        url = reverse("cart:cart-detail", args=(response.data["id"],))

        products = [self.time_slot_sale2, self.time_slot_sale5, self.store_package_1]
        data = {"products": [i.id for i in products], }

        response = client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)





