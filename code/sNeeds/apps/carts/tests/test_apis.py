from django.utils import timezone
import time

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from sNeeds.apps.account.models import Country, University, FieldOfStudy
from sNeeds.apps.carts.models import Cart
from sNeeds.apps.carts.serializers import CartSerializer
from sNeeds.apps.customAuth.models import ConsultantProfile
from sNeeds.apps.store.models import TimeSlotSale

User = get_user_model()


# from sNeeds.apps.carts.models import Cart

class CartTests(APITestCase):
    def setUp(self):
        # Users -------
        self.user1 = User.objects.create_user(email="u1@g.com", password="user1234")
        self.user1.is_admin = False
        self.user1.set_user_type_student()

        self.user2 = User.objects.create_user(email="u2@g.com", password="user1234")
        self.user2.is_admin = False
        self.user2.set_user_type_student()

        # Countries -------
        self.country1 = Country.objects.create(
            name="country1",
            slug="country1",
            picture=None
        )

        self.country2 = Country.objects.create(
            name="country2",
            slug="country2",
            picture=None
        )

        # Universities -------
        self.university1 = University.objects.create(
            name="university1",
            country=self.country1,
            description="Test desc1",
            picture=None,
            slug="university1"
        )

        self.university2 = University.objects.create(
            name="university2",
            country=self.country2,
            description="Test desc2",
            picture=None,
            slug="university2"
        )

        # Field of Studies -------
        self.field_of_study1 = FieldOfStudy.objects.create(
            name="field of study1",
            description="Test desc1",
            picture=None,
            slug="field-of-study1"
        )

        self.field_of_study2 = FieldOfStudy.objects.create(
            name="field of study2",
            description="Test desc2",
            picture=None,
            slug="field-of-study2"
        )

        # Consultants -------
        self.consultant1 = User.objects.create_user(email="c1@g.com", password="user1234")
        self.consultant1.is_admin = False
        self.consultant1.set_user_type_consultant()
        self.consultant1_profile = ConsultantProfile.objects.create(
            user=self.consultant1,
            bio="bio1",
            profile_picture=None,
            aparat_link="https://www.aparat.com/v/vG4QC",
            resume=None,
            slug="consultant1",
            active=True,
            time_slot_price=100
        )
        self.consultant1_profile.universities.set([self.university1, self.university2])
        self.consultant1_profile.field_of_studies.set([self.field_of_study1])
        self.consultant1_profile.countries.set([self.country1])

        self.consultant2 = User.objects.create_user(email="c2@g.com", password="user1234")
        self.consultant2.is_admin = False
        self.consultant2.set_user_type_consultant()
        self.consultant2_profile = ConsultantProfile.objects.create(
            user=self.consultant2,
            bio="bio2",
            profile_picture=None,
            aparat_link="https://www.aparat.com/v/vG4QC",
            resume=None,
            slug="consultant2",
            active=True,
            time_slot_price=80
        )

        # TimeSlotSales -------
        self.time_slot_sale1 = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(hours=1),
            end_time=timezone.now() + timezone.timedelta(hours=2),
            price=self.consultant1_profile.time_slot_price
        )
        self.time_slot_sale2 = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(hours=2),
            end_time=timezone.now() + timezone.timedelta(hours=3),
            price=self.consultant1_profile.time_slot_price
        )
        self.time_slot_sale3 = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=1, hours=1),
            price=self.consultant1_profile.time_slot_price
        )
        self.time_slot_sale4 = TimeSlotSale.objects.create(
            consultant=self.consultant2_profile,
            start_time=timezone.now() + timezone.timedelta(hours=1),
            end_time=timezone.now() + timezone.timedelta(hours=2),
            price=self.consultant2_profile.time_slot_price
        )
        self.time_slot_sale5 = TimeSlotSale.objects.create(
            consultant=self.consultant2_profile,
            start_time=timezone.now() + timezone.timedelta(hours=7),
            end_time=timezone.now() + timezone.timedelta(hours=8),
            price=self.consultant2_profile.time_slot_price
        )

        # Carts -------
        self.cart1 = Cart.objects.create(user=self.user1)
        self.cart1.products.set([self.time_slot_sale1, self.time_slot_sale2])

        self.cart2 = Cart.objects.create(user=self.user1)
        self.cart2.products.set([self.time_slot_sale1, self.time_slot_sale3])

        self.cart3 = Cart.objects.create(user=self.user2)
        self.cart3.products.set([self.time_slot_sale1, self.time_slot_sale5])

        # Setup ------
        self.client = APIClient()

    def test_get_cart(self):
        url = reverse("cart:cart-list")
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        response = client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for item in response.data:
            self.assertEqual(item.get("user"), self.user1.id)

        self.assertEqual(len(response.data), Cart.objects.filter(user=self.user1).count())

    def test_post_cart_pass(self):
        url = reverse("cart:cart-list")
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        products = [self.time_slot_sale1, self.time_slot_sale2, self.time_slot_sale5]
        data = {"products": [i.id for i in products], }
        response = client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertListEqual(
            [i.id for i in products].sort(),
            response.data.get("products").sort()
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

        products = [self.time_slot_sale1, self.time_slot_sale2, self.time_slot_sale5]
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
        cart = self.cart1
        url = reverse("cart:cart-detail", args=(cart.id,))
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cart.total, response.data.get("total"))
        self.assertEqual(cart.subtotal, response.data.get("subtotal"))
        self.assertEqual([p.id for p in cart.products.all()].sort(), response.data.get("products").sort())
