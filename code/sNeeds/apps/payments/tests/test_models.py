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
from sNeeds.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


class ConsultantDepositInfoAPITests(CustomAPITestCase):
    def setUp(self):
        super().setUp()

        self.client = APIClient()

    def test_consultant_deposit_info_create_correct(self):
        consultant_deposit_info_1 = ConsultantDepositInfo.objects.create(consultant=self.consultant1_profile,
                                                                         amount=400)
        self.assertIsNotNone(consultant_deposit_info_1.consultant_deposit_info_id)
        self.assertEqual(consultant_deposit_info_1.amount, 400)
