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
from sNeeds.apps.store.models import TimeSlotSale
from sNeeds.apps.store.serializers import TimeSlotSaleSerializer
from sNeeds.apps.storePackages.models import (
    StorePackagePhase, StorePackagePhaseThrough, StorePackage,
    SoldStorePackage, SoldStorePaidPackagePhase, SoldStoreUnpaidPackagePhase
)

User = get_user_model()


class CustomAPITestCase(APITestCase):
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

        # StorePackages ------
        self.store_package_1 = StorePackage.objects.create(
            title="Math Gold Package",
            slug="math-gold-package"
        )

        self.store_package_2 = StorePackage.objects.create(
            title="College Package",
            slug="college-package"
        )

        self.store_package_phase_1 = StorePackagePhase.objects.create(
            title="General Package Phase 1",
            detailed_title="General Package Phase",
            price=100
        )
        self.store_package_1_phase_2 = StorePackagePhase.objects.create(
            title="Math Gold Package Phase 2",
            detailed_title="Math Gold Phase",
            price=200
        )
        self.store_package_1_phase_3 = StorePackagePhase.objects.create(
            title="Math Gold Package Phase 3",
            detailed_title="Math Gold Phase",
            price=400
        )
        self.store_package_2_phase_2 = StorePackagePhase.objects.create(
            title="College Package Phase 2",
            detailed_title="College Phase",
            price=200
        )

        self.store_package_1_phase_through_1 = StorePackagePhaseThrough.objects.create(
            store_package=self.store_package_1,
            store_package_phase=self.store_package_phase_1,
            phase_number=1
        )
        self.store_package_1_phase_through_2 = StorePackagePhaseThrough.objects.create(
            store_package=self.store_package_1,
            store_package_phase=self.store_package_1_phase_2,
            phase_number=2
        )
        self.store_package_1_phase_through_3 = StorePackagePhaseThrough.objects.create(
            store_package=self.store_package_1,
            store_package_phase=self.store_package_1_phase_3,
            phase_number=3
        )
        self.store_package_2_phase_through_1 = StorePackagePhaseThrough.objects.create(
            store_package=self.store_package_2,
            store_package_phase=self.store_package_phase_1,
            phase_number=1
        )
        self.store_package_2_phase_through_2 = StorePackagePhaseThrough.objects.create(
            store_package=self.store_package_2,
            store_package_phase=self.store_package_2_phase_2,
            phase_number=2
        )

        self.sold_store_package_1 = SoldStorePackage.objects.create(
            title="Math Gold Package",
            sold_to=self.user1,
        )

        self.sold_store_paid_package_phase_1 = SoldStorePaidPackagePhase.objects.create(
            title=self.store_package_phase_1.title,
            detailed_title=self.store_package_phase_1.detailed_title,
            phase_number=1,
            consultant_done=True,
            sold_store_package=self.sold_store_package_1,
            price=self.store_package_phase_1.price
        )
        self.sold_store_paid_package_phase_2 = SoldStorePaidPackagePhase.objects.create(
            title=self.store_package_1_phase_2.title,
            detailed_title=self.store_package_1_phase_2.detailed_title,
            phase_number=2,
            consultant_done=False,
            sold_store_package=self.sold_store_package_1,
            price=self.store_package_1_phase_2.price
        )
        self.sold_store_unpaid_package_phase_3 = SoldStoreUnpaidPackagePhase.objects.create(
            title=self.store_package_1_phase_3.title,
            detailed_title=self.store_package_1_phase_3.detailed_title,
            phase_number=3,
            sold_store_package=self.sold_store_package_1,
            price=self.store_package_1_phase_3.price
        )

        # Carts -------
        self.cart1 = Cart.objects.create(user=self.user1)
        self.cart1.products.set([self.time_slot_sale1, self.time_slot_sale2])

        self.cart2 = Cart.objects.create(user=self.user1)
        self.cart2.products.set([self.time_slot_sale1, self.time_slot_sale3, self.store_package_1])

        self.cart3 = Cart.objects.create(user=self.user2)
        self.cart3.products.set([self.time_slot_sale1, self.time_slot_sale5])

        # Setup ------
        self.client = APIClient()
