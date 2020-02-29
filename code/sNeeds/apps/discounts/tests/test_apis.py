from django.utils import timezone
import time

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from sNeeds.apps.account.models import Country, University, FieldOfStudy
from sNeeds.apps.carts.models import Cart
from sNeeds.apps.carts.serializers import CartSerializer
from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.discounts.models import ConsultantDiscount, CartConsultantDiscount, TimeSlotSaleNumberDiscount
from sNeeds.apps.discounts.serializers import ConsultantDiscountSerializer
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

        # Consultant discounts
        self.consultant_discount1 = ConsultantDiscount.objects.create(
            percent=10,
            code="discountcode1",
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=1),
        )
        self.consultant_discount1.consultants.set([self.consultant1_profile, self.consultant2_profile])

        self.consultant_discount2 = ConsultantDiscount.objects.create(
            percent=20,
            code="discountcode2",
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=1),
        )
        self.consultant_discount2.consultants.set([self.consultant1_profile, ])

        # Cart consultant discounts
        self.cart_consultant_discount1 = CartConsultantDiscount.objects.create(
            cart=self.cart1,
            consultant_discount=self.consultant_discount1
        )

        # Setup ------
        self.client = APIClient()

    def test_cart_consultant_discounts_list_number(self):
        CartConsultantDiscount.objects.create(
            cart=self.cart3,
            consultant_discount=self.consultant_discount2
        )

        url = reverse("discount:cart-consultant-discounts-list")
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        response = client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("cart"), self.cart1.id)

    def test_cart_consultant_discounts_list_get_query_parameter(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        CartConsultantDiscount.objects.create(
            cart=self.cart2,
            consultant_discount=self.consultant_discount2
        )
        # Test 1
        url = reverse("discount:cart-consultant-discounts-list")
        response = client.get(url, {}, format='json')
        self.assertEqual(len(response.data), 2)

        # Test 2
        url = "%s?%s=%i" % (
            reverse("discount:cart-consultant-discounts-list"), "cart", self.cart_consultant_discount1.cart.id)
        response = client.get(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("cart"), self.cart1.id)

    def test_cart_consultant_discounts_list_get_query_parameter_permission(self):
        client = self.client
        client.login(email='u2@g.com', password='user1234')

        url = "%s?%s=%s" % (
            reverse("discount:cart-consultant-discounts-list"), "cart", str(self.cart_consultant_discount1.cart.id))
        response = client.get(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_cart_consultant_discount_post(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        url = reverse("discount:cart-consultant-discounts-list")
        post_data = {
            "cart": self.cart2.id,
            "code": self.consultant_discount1.code
        }
        response = client.post(url, post_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['cart'], self.cart2.id)
        self.assertEqual(response.data['code'], self.consultant_discount1.code)
        self.assertDictEqual(response.data['consultant_discount'],
                             ConsultantDiscountSerializer(self.consultant_discount1).data)

    def test_cart_consultant_discount_post_fail_unauthorized(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        url = reverse("discount:cart-consultant-discounts-list")
        post_data = {
            "cart": self.cart3.id,
            "code": self.consultant_discount1.code
        }
        response = client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cart_consultant_discount_post_fail_more_than_one_discount_on_one_cart(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        url = reverse("discount:cart-consultant-discounts-list")
        post_data = {
            "cart": self.cart1.id,
            "code": self.consultant_discount2.code
        }
        response = client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cart_consultant_discount_post_fail_no_relevant_product_in_cart(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        temp_cart = Cart.objects.create(user=self.user1)
        temp_cart.products.set([self.time_slot_sale1, self.time_slot_sale2])

        temp_consultant_discount = ConsultantDiscount.objects.create(
            percent=20,
            code="temp_consultant_discount",
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=1),
        )
        temp_consultant_discount.consultants.set([self.consultant2_profile])

        url = reverse("discount:cart-consultant-discounts-list")
        post_data = {
            "cart": temp_cart.id,
            "code": temp_consultant_discount.code
        }

        response = client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cart_consultant_discount_correct_total_subtotal_update_1(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        temp_cart = Cart.objects.create(user=self.user1)
        temp_cart.products.set([self.time_slot_sale1, self.time_slot_sale2])

        temp_consultant_discount = ConsultantDiscount.objects.create(
            percent=20,
            code="temp_consultant_discount",
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=1),
        )
        temp_consultant_discount.consultants.set([self.consultant1_profile, self.consultant2_profile])

        url = reverse("discount:cart-consultant-discounts-list")
        post_data = {
            "cart": temp_cart.id,
            "code": temp_consultant_discount.code
        }

        response = client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse("cart:cart-detail", args=(temp_cart.id,))
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("total"), 160)
        self.assertEqual(response.data.get("subtotal"), 200)

    def test_cart_consultant_discount_correct_total_subtotal_update_2(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        temp_cart = Cart.objects.create(user=self.user1)
        temp_cart.products.set([self.time_slot_sale1, self.time_slot_sale4])

        temp_consultant_discount = ConsultantDiscount.objects.create(
            percent=20,
            code="temp_consultant_discount",
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=1),
        )
        temp_consultant_discount.consultants.set([self.consultant1_profile, ])

        url = reverse("discount:cart-consultant-discounts-list")
        post_data = {
            "cart": temp_cart.id,
            "code": temp_consultant_discount.code
        }

        response = client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse("cart:cart-detail", args=(temp_cart.id,))
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("total"), 160)
        self.assertEqual(response.data.get("subtotal"), 180)

    def test_cart_consultant_discount_detail_get(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        url = reverse("discount:cart-consultant-discount-detail", args=(self.cart_consultant_discount1.id,))
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("cart"), self.cart_consultant_discount1.cart.id)

    def test_cart_consultant_discount_detail_get_no_permission(self):
        client = self.client
        client.login(email='u2@g.com', password='user1234')

        url = reverse("discount:cart-consultant-discount-detail", args=(self.cart_consultant_discount1.id,))
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cart_consultant_discount_detail_get_unauthorized(self):
        client = self.client

        url = reverse("discount:cart-consultant-discount-detail", args=(self.cart_consultant_discount1.id,))
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cart_consultant_discount_detail_delete(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        url = reverse("discount:cart-consultant-discount-detail", args=(self.cart_consultant_discount1.id,))
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cart_consultant_discount_detail_delete_no_permission(self):
        client = self.client
        client.login(email='u2@g.com', password='user1234')

        url = reverse("discount:cart-consultant-discount-detail", args=(self.cart_consultant_discount1.id,))
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cart_consultant_discount_detail_delete_unauthorized(self):
        client = self.client

        url = reverse("discount:cart-consultant-discount-detail", args=(self.cart_consultant_discount1.id,))
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cart_consultant_discount_delete_updates_cart_total_subtotal(self):
        self.assertEqual(self.cart1.total, 180)
        self.assertEqual(self.cart1.subtotal, 200)
        self.cart_consultant_discount1.delete()
        self.assertEqual(self.cart1.total, 200)
        self.assertEqual(self.cart1.total, 200)

    def test_cart_consultant_discount_delete_updates_cart_total_subtotal(self):
        self.assertEqual(self.cart1.total, 180)
        self.assertEqual(self.cart1.subtotal, 200)
        self.cart_consultant_discount1.delete()
        self.assertEqual(self.cart1.total, 200)
        self.assertEqual(self.cart1.total, 200)

    def test_time_slot_sale_number_discount_correct_cart_total_subtotal(self):
        self.assertEqual(self.cart1.total, 180)
        self.assertEqual(self.cart1.subtotal, 200)

        time_slot_sale_number_discount_1 = TimeSlotSaleNumberDiscount.objects.create(
            number=2,
            discount=50
        )

        # self.cart was not updating!
        self.assertEqual(Cart.objects.get(id=self.cart1.id).total, 90)
        self.assertEqual(Cart.objects.get(id=self.cart1.id).subtotal, 200)

        time_slot_sale_number_discount_1.delete()

        # self.cart was not updating!
        self.assertEqual(Cart.objects.get(id=self.cart1.id).total, 180)
        self.assertEqual(Cart.objects.get(id=self.cart1.id).subtotal, 200)
