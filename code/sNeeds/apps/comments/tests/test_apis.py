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
from sNeeds.apps.discounts.serializers import DiscountSerializer
from sNeeds.apps.orders.models import Order
from sNeeds.apps.store.models import TimeSlotSale, SoldTimeSlotSale
from sNeeds.apps.store.tasks import delete_time_slots

from sNeeds.settings.celery.celery import app

User = get_user_model()


# from sNeeds.apps.carts.models import Cart

class CartTests(APITestCase):
    allow_database_queries = True

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

    def test_consultant_list_get_success(self):
        client = self.client
        url = reverse("comments:comment-list")

        response = client.get(url, format="json")

        self.assertEqual(len(response.data), len(ConsultantComment.objects.all()))

    def test_consultant_list_filter_user_get_success(self):
        client = self.client
        url = "%s?%s=%s" % (
            reverse("comments:comment-list"),
            "user",
            self.user1.id
        )

        response = client.get(url, format="json")

        self.assertEqual(len(response.data), 2)

    def test_consultant_list_filter_consultant_get_success(self):
        client = self.client
        url = "%s?%s=%s" % (
            reverse("comments:comment-list"),
            "consultant",
            self.consultant1_profile.id
        )

        response = client.get(url, format="json")

        self.assertEqual(len(response.data), 1)

    def test_consultant_list_post_success(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')
        url = reverse("comments:comment-list")

        consultant_comment_before_count = ConsultantComment.objects.all().count()
        data = {
            "consultant": self.consultant1_profile.id,
            "message": "hello"
        }
        response = client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ConsultantComment.objects.all().count(), consultant_comment_before_count + 1)
        self.assertEqual(response.data.get("user").get("id"), self.user1.id)

    def test_consultant_list_post_permission_fail(self):
        client = self.client
        url = reverse("comments:comment-list")

        data = {
            "consultant": self.consultant1_profile.id,
            "message": "hello"
        }
        response = client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_consultant_detail_get_success(self):
        client = self.client
        c1 = self.consultant_comment1

        url = reverse("comments:comment-detail", args=(c1.id,))
        response = client.get(url, format='json')
        data = response.data

        self.assertEqual(data.get("id"), c1.id)
        self.assertEqual(data.get("user").get("id"), c1.user.id)
        self.assertEqual(data.get("user").get("first_name"), c1.user.first_name)
        self.assertEqual(data.get("user").get("last_name"), c1.user.last_name)
        self.assertEqual(data.get("admin_reply"), "Admin message 1")
        self.assertEqual(data.get("consultant"), c1.consultant.id)
        self.assertEqual(data.get("message"), c1.message)
        self.assertEqual(data.get("created"), serializers.DateTimeField().to_representation(c1.created))
        self.assertEqual(data.get("updated"), serializers.DateTimeField().to_representation(c1.updated))

        url = reverse("comments:comment-detail", args=(self.consultant_comment3.id,))
        response = client.get(url, format='json')
        data = response.data

        self.assertEqual(data.get("admin_reply"), None)

    def test_sold_time_slot_rate_list_get_success(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        url = reverse("comments:sold-time-slot-rate-list")
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            SoldTimeSlotRate.objects.filter(sold_time_slot__sold_to=self.user1).count() + \
            SoldTimeSlotRate.objects.filter(sold_time_slot__consultant__user=self.user1).count()
        )

    def test_sold_time_slot_rate_get_filter_by_sold_time_slot_success(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')
        url = "%s?%s=%s" % (
            reverse("comments:sold-time-slot-rate-list"),
            "sold_time_slot",
            self.sold_time_slot_sale1.id
        )
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("sold_time_slot"), self.sold_time_slot_sale1.id)

    def test_sold_time_slot_rate_get_filter_by_sold_time_slot_fail(self):
        client = self.client
        url = "%s?%s=%s" % (
            reverse("comments:sold-time-slot-rate-list"),
            "sold_time_slot",
            self.sold_time_slot_sale3.id
        )
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sold_time_slot_rate_list_post_success(self):
        client = self.client
        client.login(email='u2@g.com', password='user1234')

        url = reverse("comments:sold-time-slot-rate-list")

        before_count = SoldTimeSlotRate.objects.all().count()
        data = {
            "sold_time_slot": self.sold_time_slot_sale3.id,
            "rate": 1
        }
        response = client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            before_count + 1,
            SoldTimeSlotRate.objects.all().count()
        )

    def test_sold_time_slot_rate_list_post_permission_denied(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        url = reverse("comments:sold-time-slot-rate-list")

        data = {
            "sold_time_slot": self.sold_time_slot_sale3.id,
            "rate": 1
        }
        response = client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
