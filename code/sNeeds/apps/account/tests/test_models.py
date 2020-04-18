from rest_framework.test import APITestCase
from sNeeds.apps.account.models import StudentDetailedInfo, FieldOfStudy, University, Country
from sNeeds.apps.consultants.models import ConsultantProfile

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from sNeeds.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


class StudentDetailedInfoTests(CustomAPITestCase):

    def setUp(self):
        super().setUp()

    def test_create_student_detailed_info_successful(self):
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
            "language_listening": 50,
            "language_writing": 50,
            "language_reading": 50,
            "mainland": "asia",
            "country": "america",
            "apply_grade": "college",
            "apply_major": "tashtak sazi",
            "comment": "HEllllo",
        }
        student_detailed_info = StudentDetailedInfo.objects.create(**payload)
        keys = payload.keys()
        for key in keys:
            self.assertEqual(payload[key], getattr(student_detailed_info, key))
