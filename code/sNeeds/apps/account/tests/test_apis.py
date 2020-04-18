import datetime

from rest_framework.test import APITestCase, APIClient

from sNeeds.apps.account.models import StudentDetailedInfo, FieldOfStudy, University, Country
from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.store.models import SoldTimeSlotSale
from sNeeds.apps.storePackages.models import SoldStorePackage

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from rest_framework import status

from sNeeds.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


class StudentDetailedInfoTests(CustomAPITestCase):

    def setUp(self):
        super().setUp()

        payload = {
            "user": self.user1,
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
        self.student_detailed_info1 = StudentDetailedInfo.objects.create(**payload)

        self.client = APIClient()

    def test_list_post_success_valid_credentials_set_user_correct(self):
        url = reverse('account:student-detailed-info-list')
        client = self.client
        # client.login(email=self.user1.email, password=self.user1.password)
        client.force_login(self.user2)
        payload = {
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

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user2.id)

    def test_list_post_fail_invalid_marital_status(self):
        url = reverse('account:student-detailed-info-list')
        client = self.client
        # client.login(email=self.user1.email, password=self.user1.password)
        client.force_login(self.user2)
        payload = {
            "first_name": "u1",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "marrlnlnied",
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

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_post_fail_invalid_grade_status(self):
        url = reverse('account:student-detailed-info-list')
        client = self.client
        # client.login(email=self.user1.email, password=self.user1.password)
        client.force_login(self.user2)
        payload = {
            "first_name": "u1",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "single",
            "grade": "post_doctoral",
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

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_post_fail_invalid_language_speaking(self):
        url = reverse('account:student-detailed-info-list')
        client = self.client
        # client.login(email=self.user1.email, password=self.user1.password)
        client.force_login(self.user2)
        payload = {
            "first_name": "u1",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "single",
            "grade": "doctoral",
            "university": "payamnoor",
            "total_average": "16.20",
            "degree_conferral_year": 2022,
            "major": "memari jolbak",
            "thesis_title": "kasht jolbak dar darya",
            "language_certificate": "ielts_academic",
            "language_certificate_overall": 50,
            "language_speaking": 500,
            "language_listening": 10,
            "language_writing": 50,
            "language_reading": 50,
            "mainland": "asia",
            "country": "america",
            "apply_grade": "college",
            "apply_major": "tashtak sazi",
            "comment": "HEllllo",
        }

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_multi_student_info_fail(self):
        url = reverse('account:student-detailed-info-list')
        client = self.client
        # client.login(email=self.user1.email, password=self.user1.password)
        client.force_login(self.user1)
        payload = {
            "first_name": "u1",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "single",
            "grade": "doctoral",
            "university": "payamnoor",
            "total_average": "16.20",
            "degree_conferral_year": 2022,
            "major": "memari jolbak",
            "thesis_title": "kasht jolbak dar darya",
            "language_certificate": "ielts_academic",
            "language_certificate_overall": 50,
            "language_speaking": 10,
            "language_listening": 10,
            "language_writing": 50,
            "language_reading": 50,
            "mainland": "asia",
            "country": "america",
            "apply_grade": "college",
            "apply_major": "tashtak sazi",
            "comment": "HEllllo",
        }
        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_consultant_post_method_fail(self):
        url = reverse('account:student-detailed-info-list')
        client = self.client
        # client.login(email=self.user1.email, password=self.user1.password)
        client.force_login(self.consultant1)
        payload = {
            "first_name": "u1",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "single",
            "grade": "doctoral",
            "university": "payamnoor",
            "total_average": "16.20",
            "degree_conferral_year": 2022,
            "major": "memari jolbak",
            "thesis_title": "kasht jolbak dar darya",
            "language_certificate": "ielts_academic",
            "language_certificate_overall": 50,
            "language_speaking": 10,
            "language_listening": 10,
            "language_writing": 50,
            "language_reading": 50,
            "mainland": "asia",
            "country": "america",
            "apply_grade": "college",
            "apply_major": "tashtak sazi",
            "comment": "HEllllo",
        }
        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_consultant_get_fail(self):
        url = reverse('account:student-detailed-info-list')
        client = self.client
        client.force_login(self.consultant1)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_put_patch_delete_denied(self):
        url = reverse('account:student-detailed-info-list')
        client = self.client
        # client.login(email=self.user1.email, password=self.user1.password)
        client.force_login(self.user2)
        payload = {
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

        response = client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = client.delete(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_detail_owner_patch_success(self):
        url = reverse('account:student-detailed-info-detail', args=(self.student_detailed_info1.id,))
        client = self.client
        client.force_login(self.user1)
        payload = {
            "first_name": "akbar",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "married",
            "grade": "college",
            "university": "payamnoor",
            "total_average": "17.00",
            "degree_conferral_year": 2022,
            "major": "memari jolbak",
            "thesis_title": "kasht jolbak dar darya",
            "language_certificate": "ielts_academic",
            "language_certificate_overall": 50,
            "language_speaking": 56,
            "mainland": "asia",
            "country": "america",
            "apply_grade": "college",
            "apply_major": "tashtak sazi",
        }

        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("first_name"), payload.get("first_name"))
        self.assertEqual(response.data.get("total_average"), payload.get("total_average"))
        self.assertEqual(response.data.get("language_speaking"), payload.get("language_speaking"))

    def test_detail_owner_update_success(self):
        url = reverse('account:student-detailed-info-detail', args=(self.student_detailed_info1.id,))
        client = self.client
        client.force_login(self.user1)
        payload = {
            "first_name": "asghar",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "married",
            "grade": "college",
            "university": "payamnoor",
            "total_average": "9.10",
            "degree_conferral_year": 2022,
            "major": "memari jolbak",
            "thesis_title": "kasht jolbak dar darya",
            "language_certificate": "ielts_academic",
            "language_certificate_overall": 50,
            "language_speaking": 20,
            "language_listening": 10,
            "language_writing": 50,
            "language_reading": 50,
            "mainland": "asia",
            "country": "america",
            "apply_grade": "college",
            "apply_major": "tashtak sazi",
            "comment": "HEllllo",
        }

        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("first_name"), payload.get("first_name"))
        self.assertEqual(response.data.get("total_average"), payload.get("total_average"))
        self.assertEqual(response.data.get("language_speaking"), payload.get("language_speaking"))

    def test_detail_patch_change_user_denied(self):
        url = reverse('account:student-detailed-info-detail', args=(self.student_detailed_info1.id,))
        client = self.client
        client.force_login(self.user1)
        # print(self.student_detailed_info1.user.id)
        payload = {
            "user": self.user2.id
        }

        response = client.patch(url, payload)
        # print(response.data.get("user"))
        # print(self.student_detailed_info1.user.id)
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.student_detailed_info1.user.id, self.user1.id)

    def test_detail_other_users_detail_get_patch_put_fail(self):
        url = reverse('account:student-detailed-info-detail', args=(self.student_detailed_info1.id,))
        client = self.client
        client.force_login(self.user2)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        payload = {
            "first_name": "asghar",
            "last_name": "u1u1",
            "age": 19,
            "marital_status": "married",
            "grade": "college",
        }

        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_interactive_consultant_time_slot_get_success_patch_fail(self):
        url = reverse('account:student-detailed-info-detail', args=(self.student_detailed_info1.id,))
        client = self.client
        client.force_login(self.consultant1)

        SoldTimeSlotSale.objects.create(consultant=self.consultant1_profile, sold_to=self.user1,
                                        price=5000, start_time=timezone.now(),
                                        end_time=timezone.now() + timezone.timedelta(hours=2))

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = {
            "first_name": "asghar",
            "last_name": "u1u1",
        }
        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_interactive_consultant_store_package_get_success_patch_fail(self):
        url = reverse('account:student-detailed-info-detail', args=(self.student_detailed_info1.id,))
        client = self.client
        client.force_login(self.consultant1)

        SoldStorePackage.objects.create(consultant=self.consultant1_profile, sold_to=self.user1,
                                        paid_price=5000, total_price=15000, title="Hello")

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = {
            "first_name": "asghar",
            "last_name": "u1u1",
        }
        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_interactive_consultant_get_patch_method_fail(self):
        url = reverse('account:student-detailed-info-detail', args=(self.student_detailed_info1.id,))
        client = self.client
        client.force_login(self.consultant1)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        payload = {
            "first_name": "asghar",
            "last_name": "u1u1",
        }
        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
