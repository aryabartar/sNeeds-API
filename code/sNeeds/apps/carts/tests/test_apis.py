from django.utils import timezone
import time

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from sNeeds.apps.account.models import Country, University, FieldOfStudy
from sNeeds.apps.customAuth.models import ConsultantProfile
from sNeeds.apps.store.models import TimeSlotSale

User = get_user_model()


# from sNeeds.apps.carts.models import Cart

class CartTests(APITestCase):
    def setUp(self):
        def create_users(self):
            self.user1 = User.objects.create_user(email="u1@g.com", password="user1234")
            self.user1.is_admin = False
            self.user1.set_user_type_student()

            self.user2 = User.objects.create_user(email="u2@g.com", password="user1234")
            self.user2.is_admin = False
            self.user2.set_user_type_student()

        def create_countries(self):
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

        def create_universities(self):
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

        def create_field_of_studies(self):
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

        def create_consultants(self):
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

            self.time_slot_sale1 = TimeSlotSale.objects.create(
                consultant=self.consultant1_profile,
                start_time=timezone.now() + timezone.timedelta(hours=1),
                end_time=timezone.now() + timezone.timedelta(hours=2),
                price=self.consultant1_profile.time_slot_price
            )

            self.time_slot_sale2 = TimeSlotSale.objects.create(
                consultant=self.consultant1_profile,
                start_time=timezone.now() + timezone.timedelta(hours=3),
                end_time=timezone.now() + timezone.timedelta(hours=4),
                price=self.consultant1_profile.time_slot_price
            )

            self.time_slot_sale3 = TimeSlotSale.objects.create(
                consultant=self.consultant1_profile,
                start_time=timezone.now() + timezone.timedelta(days=1),
                end_time=timezone.now() + timezone.timedelta(days=1, hours=1),
                price=self.consultant1_profile.time_slot_price
            )

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

        create_users(self)
        create_countries(self)
        create_universities(self)
        create_field_of_studies(self)
        create_consultants(self)

        self.client = APIClient()

    def test_one_plus_one_equals_two(self):
        print(User.objects.all())
