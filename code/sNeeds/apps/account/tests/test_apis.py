from rest_framework.test import APITestCase, APIClient
from sNeeds.apps.account.models import StudentDetailedInfo, FieldOfStudy, University, Country
from sNeeds.apps.consultants.models import ConsultantProfile

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

User = get_user_model()


class StudentDetailedInfoTests(APITestCase):

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

        self.client = APIClient()

    def test_create_student_detailed_info_success_valid_credentials_set_user_correct(self):
        url = reverse('account:student-detailed-info-list')
        client = self.client
        # client.login(email=self.user1.email, password=self.user1.password)
        client.force_login(self.user1)
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
        self.assertEqual(response.data.get('user'), self.user1.id)

    def test_create_student_detailed_info_fail_invalid_marital_status(self):
        url = reverse('account:student-detailed-info-list')
        client = self.client
        # client.login(email=self.user1.email, password=self.user1.password)
        client.force_login(self.user1)
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