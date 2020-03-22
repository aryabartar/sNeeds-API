from django.utils import timezone

from sNeeds.apps.consultants.models import ConsultantProfile
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from sNeeds.apps.account.models import Country, University, FieldOfStudy
from sNeeds.apps.carts.models import Cart
from sNeeds.apps.discounts.models import Discount, CartDiscount, TimeSlotSaleNumberDiscount
from sNeeds.apps.discounts.serializers import DiscountSerializer
from sNeeds.apps.store.models import TimeSlotSale
from sNeeds.apps.customForms.models import BugReport

User = get_user_model()


class BugReportTests(APITestCase):
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

        # self.cart4 = Cart.objects.create(user=self.user1)
        # self.cart4.products.set([self.webinar1])

        # self.cart5 = Cart.objects.create(user=self.user1)
        # self.cart5.products.set([self.webinar2])
        #
        # self.cart6 = Cart.objects.create(user=self.user1)
        # self.cart6.products.set([self.webinar1, self.webinar2])

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
        self.discount3.products.set([self.webinar1])

        # Cart consultant discounts
        self.cart_discount1 = CartDiscount.objects.create(
            cart=self.cart1,
            discount=self.discount1
        )

        # Setup ------
        self.client = APIClient()

    def test_create_bug_report_logged_in_user_entered_email_again(self):
        client = self.client
        client.login(email='zx@gmial.com', password='123password')
        url = reverse('customForms:bug-report-create')

        post_data = {
            "email": "qw@gmail.com",
            "comment": "shop is not working",
        }
        response = client.post(url, post_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("email"), post_data.get("email"))
        self.assertEqual(response.data.get("comment"), post_data.get("comment"))

    def test_create_bug_report_logged_in_user_not_entered_email_again(self):
        client = self.client
        client.force_login(user=self.user1)
        url = reverse('customForms:bug-report-create')

        post_data = {
            "comment": "shop is not working",
        }
        response = client.post(url, post_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("email"), self.user1.email)
        self.assertEqual(response.data.get("comment"), post_data.get("comment"))

    def test_create_bug_report_fail_with_no_comment(self):
        client = self.client
        client.login(email='zx@gmial.com', password='123password')
        url = reverse('customForms:bug-report-create')

        post_data = {
            "email": "yu@gmail.com",
        }
        response = client.post(url, post_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_bug_report_is_not_allowed(self):
        client = self.client
        client.login(email='zx@gmial.com', password='123password')
        url = reverse('customForms:bug-report-create')

        post_data = {
            "email": "yu@gmail.com",
        }
        response = client.get(url, post_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)