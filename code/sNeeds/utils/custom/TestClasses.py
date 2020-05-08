from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import time

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.conf import settings

from sNeeds.apps.account.models import Country, University, FieldOfStudy, StudentDetailedInfo
from sNeeds.apps.carts.models import Cart
from sNeeds.apps.carts.serializers import CartSerializer
from sNeeds.apps.consultants.models import ConsultantProfile, StudyInfo
from sNeeds.apps.store.models import TimeSlotSale, SoldTimeSlotSale
from sNeeds.apps.store.serializers import TimeSlotSaleSerializer
from sNeeds.apps.storePackages.models import (
    StorePackagePhase, StorePackagePhaseThrough, StorePackage,
    SoldStorePackage, SoldStorePaidPackagePhase, SoldStoreUnpaidPackagePhase,
    SoldStorePackagePhaseDetail)

USER_DETAILED_INFO_BASE_PAYLOAD = {
    "first_name": "u1",
    "last_name": "u1u1",
    "age": 19,
    "marital_status": "married",
    "grade": "college",
    "university": "payamnoor",
    "total_average": "16.20",
    "degree_conferral_year": 2022,
    "major": "memari jolbak",
    "thesis_title": "kasht jolbak dar darya",
    "language_certificate": "ielts_academic",
    "language_certificate_overall": 50,
    "language_speaking": 50,
    "language_listening": 10,
    "language_writing": 50,
    "language_reading": 50,
    "mainland": "asia",
    "country": "america",
    "apply_grade": "college",
    "apply_major": "tashtak sazi",
    "comment": "HEllllo",
}

User = get_user_model()


class CustomAPITestCase(APITestCase):
    def setUp(self):
        # Configs
        settings.SKYROOM_API_KEY = None

        # Users -------
        self.user1 = User.objects.create_user(email="u1@g.com", password="user1234", first_name="User 1")
        self.user1.is_admin = False
        self.user1.set_user_type_student()

        self.user2 = User.objects.create_user(email="u2@g.com", password="user1234", first_name="User 2")
        self.user2.is_admin = False
        self.user2.set_user_type_student()

        self.user3 = User.objects.create_user(email="u3@g.com", password="user1234", first_name="User 3")
        self.user3.is_admin = False
        self.user3.set_user_type_student()

        user_1_detailed_info_payload = USER_DETAILED_INFO_BASE_PAYLOAD
        user_1_detailed_info_payload['user'] = self.user1
        self.user1_student_detailed_info = StudentDetailedInfo.objects.create(**user_1_detailed_info_payload)

        user_2_detailed_info_payload = USER_DETAILED_INFO_BASE_PAYLOAD
        user_2_detailed_info_payload['user'] = self.user2
        self.user2_student_detailed_info = StudentDetailedInfo.objects.create(**user_2_detailed_info_payload)

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

        StudyInfo.objects.create(
            consultant=self.consultant1_profile,
            university=self.university1,
            field_of_study=self.field_of_study1,
            grade="bachelor",
            order=1
        )
        StudyInfo.objects.create(
            consultant=self.consultant1_profile,
            university=self.university2,
            field_of_study=self.field_of_study1,
            grade="master",
            order=1
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
        self.time_slot_sale33 = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(days=2),
            end_time=timezone.now() + timezone.timedelta(days=2, hours=1),
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

        # SoldTimeSlotSales -------
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
            consultant=self.consultant1_profile
        )

        self.sold_store_paid_package_1_phase_1 = SoldStorePaidPackagePhase.objects.create(
            title=self.store_package_phase_1.title,
            detailed_title=self.store_package_phase_1.detailed_title,
            phase_number=1,
            consultant_done=True,
            sold_store_package=self.sold_store_package_1,
            price=self.store_package_phase_1.price
        )
        self.sold_store_paid_package_1_phase_2 = SoldStorePaidPackagePhase.objects.create(
            title=self.store_package_1_phase_2.title,
            detailed_title=self.store_package_1_phase_2.detailed_title,
            phase_number=2,
            consultant_done=False,
            sold_store_package=self.sold_store_package_1,
            price=self.store_package_1_phase_2.price
        )
        self.sold_store_unpaid_package_1_phase_3 = SoldStoreUnpaidPackagePhase.objects.create(
            title=self.store_package_1_phase_3.title,
            detailed_title=self.store_package_1_phase_3.detailed_title,
            phase_number=3,
            sold_store_package=self.sold_store_package_1,
            price=self.store_package_1_phase_3.price
        )

        self.sold_store_package_1_phase_detail_1 = SoldStorePackagePhaseDetail.objects.create(
            title='title 1',
            status='in_progress',
            content_type=ContentType.objects.get(app_label='storePackages', model='soldstorepaidpackagephase'),
            object_id=self.sold_store_paid_package_1_phase_1.id
        )
        self.sold_store_package_1_phase_detail_2 = SoldStorePackagePhaseDetail.objects.create(
            title='title 2',
            status='done',
            content_type=ContentType.objects.get(app_label='storePackages', model='soldstorepaidpackagephase'),
            object_id=self.sold_store_paid_package_1_phase_1.id
        )
        self.sold_store_package_1_phase_detail_3 = SoldStorePackagePhaseDetail.objects.create(
            title='title 3',
            status='in_progress',
            content_type=ContentType.objects.get(app_label='storePackages', model='soldstorepaidpackagephase'),
            object_id=self.sold_store_paid_package_1_phase_2.id
        )

        self.sold_store_package_2 = SoldStorePackage.objects.create(
            title="Math Gold Package",
            sold_to=self.user2,
            consultant=None
        )

        self.sold_store_paid_package_2_phase_1 = SoldStorePaidPackagePhase.objects.create(
            title=self.store_package_phase_1.title,
            detailed_title=self.store_package_phase_1.detailed_title,
            phase_number=1,
            consultant_done=False,
            sold_store_package=self.sold_store_package_2,
            price=self.store_package_phase_1.price
        )
        self.sold_store_paid_package_2_phase_2 = SoldStoreUnpaidPackagePhase.objects.create(
            title=self.store_package_1_phase_2.title,
            detailed_title=self.store_package_1_phase_2.detailed_title,
            phase_number=2,
            sold_store_package=self.sold_store_package_2,
            price=self.store_package_1_phase_2.price
        )
        self.sold_store_unpaid_package_2_phase_3 = SoldStoreUnpaidPackagePhase.objects.create(
            title=self.store_package_1_phase_3.title,
            detailed_title=self.store_package_1_phase_3.detailed_title,
            phase_number=3,
            sold_store_package=self.sold_store_package_2,
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
