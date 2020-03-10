import json

from django.core.exceptions import ValidationError
from django.utils import timezone

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
from sNeeds.apps.storePackages.serializers import StorePackageSerializer
from sNeeds.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


class CartModelTests(CustomAPITestCase):
    def setUp(self):
        super().setUp()

    def test_cart_create_user_is_consultant_fail(self):
        with self.assertRaises(ValidationError) as e:
            Cart.objects.create(user=self.consultant1)
