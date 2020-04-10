from django.utils import timezone

from sNeeds.apps.consultants.models import ConsultantProfile
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from sNeeds.apps.account.models import Country, University, FieldOfStudy
from sNeeds.apps.carts.models import Cart
from sNeeds.apps.discounts.models import Discount, CartDiscount, TimeSlotSaleNumberDiscount
from sNeeds.apps.discounts.serializers import ShortDiscountSerializer
from sNeeds.apps.store.models import TimeSlotSale
from sNeeds.apps.basicProducts.models import BasicProduct
from sNeeds.apps.customForms.models import BugReport
from sNeeds.apps.payments.models import ConsultantDepositInfo

User = get_user_model()


class ConsultantDepositInfoAPITests(APITestCase):
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

        # BasicProducts
        self.BasicProduct1 = BasicProduct.objects.create(
            title="BasicProduct1",
            slug="BasicProduct1",
            active=True,
            price=30000,
        )

        self.BasicProduct2 = BasicProduct.objects.create(
            title="BasicProduct2",
            slug="BasicProduct2",
            active=True,
            price=30000,
        )

        self.BasicProduct3 = BasicProduct.objects.create(
            title="BasicProduct3",
            slug="BasicProduct3",
            active=True,
            price=30000,
        )

        self.BasicProduct4 = BasicProduct.objects.create(
            title="BasicProduct4",
            slug="BasicProduct4",
            active=False,
            price=30000,
        )

        # Carts -------
        self.cart1 = Cart.objects.create(user=self.user1)
        self.cart1.products.set([self.time_slot_sale1, self.time_slot_sale2])

        self.cart2 = Cart.objects.create(user=self.user1)
        self.cart2.products.set([self.time_slot_sale1, self.time_slot_sale3])

        self.cart3 = Cart.objects.create(user=self.user2)
        self.cart3.products.set([self.time_slot_sale1, self.time_slot_sale5])

        self.cart4 = Cart.objects.create(user=self.user1)
        self.cart4.products.set([self.BasicProduct1])

        self.cart5 = Cart.objects.create(user=self.user1)
        self.cart5.products.set([self.BasicProduct2])

        self.cart6 = Cart.objects.create(user=self.user1)
        self.cart6.products.set([self.BasicProduct1, self.BasicProduct2])

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

        self.discount3 = Discount.objects.create(
            amount=500,
            code="discountcode3"
        )
        self.discount3.products.set([self.BasicProduct1])

        # Cart consultant discounts
        self.cart_discount1 = CartDiscount.objects.create(
            cart=self.cart1,
            discount=self.discount1
        )

        self.consultant_deposit_info_1 = ConsultantDepositInfo.objects.create(consultant=self.consultant1_profile,
                                                                              amount=4000)
        self.consultant_deposit_info_2 = ConsultantDepositInfo.objects.create(consultant=self.consultant1_profile,
                                                                              amount=5000)
        self.consultant_deposit_info_2 = ConsultantDepositInfo.objects.create(consultant=self.consultant2_profile,
                                                                              amount=5000)

        # Setup ------
        self.client = APIClient()

    def test_list_consultant_deposit_get_success(self):
        url = reverse('payment:consultant-deposit-list')
        client = self.client
        client.force_login(self.consultant1)

        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_consultant_deposit_post_put_patch_delete_fail(self):
        url = reverse('payment:consultant-deposit-list')
        client = self.client
        client.force_login(self.consultant1)

        payload = {
            'consultant': self.consultant1.id,
            'amount': 6000,
        }

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_consultant_deposit_other_consultant_access_denied(self):
        url = reverse('payment:consultant-deposit-list')
        client = self.client
        client.force_login(self.consultant2)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_consultant_deposit_other_users_access_denied(self):
        url = reverse('payment:consultant-deposit-list')
        client = self.client
        client.force_login(self.user1)

        payload = {
            'consultant': self.consultant1.id,
            'amount': 6000,
        }

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_consultant_deposit_unauthorized_access_denied(self):
        url = reverse('payment:consultant-deposit-list')
        client = self.client

        payload = {
            'consultant': self.consultant1.id,
            'amount': 6000,
        }

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_consultant_deposit_get_success(self):
        url = reverse('payment:consultant-deposit-detail',
                      args=(self.consultant_deposit_info_1.consultant_deposit_info_id,))
        client = self.client
        client.force_login(self.consultant1)

        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_consultant_deposit_post_put_patch_delete_fail(self):
        url = reverse('payment:consultant-deposit-detail',
                      args=(self.consultant_deposit_info_1.consultant_deposit_info_id,))
        client = self.client
        client.force_login(self.consultant1)

        payload = {
            'consultant': self.consultant1.id,
            'amount': 6000,
        }

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_detail_consultant_deposit_other_consultant_access_denied(self):
        url = reverse('payment:consultant-deposit-detail',
                      args=(self.consultant_deposit_info_1.consultant_deposit_info_id,))
        client = self.client
        client.force_login(self.consultant2)

        payload = {
            'consultant': self.consultant1.id,
            'amount': 6000,
        }

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_detail_consultant_deposit_other_users_access_denied(self):
        url = reverse('payment:consultant-deposit-detail',
                      args=(self.consultant_deposit_info_1.consultant_deposit_info_id,))
        client = self.client
        client.force_login(self.user1)

        payload = {
            'consultant': self.consultant1.id,
            'amount': 6000,
        }

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_consultant_deposit_unauthorized_access_denied(self):
        url = reverse('payment:consultant-deposit-detail',
                      args=(self.consultant_deposit_info_1.consultant_deposit_info_id,))
        client = self.client

        payload = {
            'consultant': self.consultant1.id,
            'amount': 6000,
        }

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
