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
from sNeeds.apps.customForms.models import BugReport
from sNeeds.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


class BugReportTests(CustomAPITestCase):
    def setUp(self):
        super().setUp()

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
