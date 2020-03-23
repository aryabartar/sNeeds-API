from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse

from sNeeds.utils.custom.TestClasses import CustomAPITestCase
from sNeeds.apps.storePackages.models import (
    StorePackage, StorePackagePhase, StorePackagePhaseThrough, SoldStorePackage,
    SoldStoreUnpaidPackagePhase, SoldStorePaidPackagePhase
)


class TestStorePackage(CustomAPITestCase):

    def setUp(self):
        super().setUp()

        self.store_package_1 = StorePackage.objects.create(
            title="Math Gold Package",
            slug="math-gold-package"
        )

        self.store_package_1_phase_1 = StorePackagePhase.objects.create(
            title="Math Gold Package Phase 1",
            detailed_title="Math Gold"
        )


    def test_store_package_phase_through_list_get_success(self):
        client = self.client
        url = reverse("store-package:store-package-phase-through-list")

        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

    def test_store_package_phase_through_detail_get_success(self):
        client = self.client
        url = reverse("store-package:store-package-phase-through-detail", args=[self.store_package_phase_through1.id])

        response = client.get(url, format="json")

        data = response.data
        obj = self.store_package_phase_through1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("id"), obj.id)
        self.assertEqual(data.get("title"), obj.store_package_phase.title)
        self.assertEqual(data.get("store_package"), obj.store_package.id)
        self.assertEqual(data.get("phase_number"), obj.phase_number)
        self.assertEqual(data.get("price"), obj.store_package_phase.price)

    def test_store_package_list_get_success(self):
        client = self.client
        url = reverse("store-package:store-package-list")

        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_store_package_detail_get_success(self):
        client = self.client
        url = reverse("store-package:store-package-detail", args=[self.store_package1.slug, ])

        response = client.get(url, format="json")

        data = response.data
        obj = self.store_package1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), obj.title)
        self.assertEqual(len(data.get("store_package_phases")), len(obj.store_package_phases.all()))
        self.assertEqual(data.get("slug"), obj.slug)
        self.assertEqual(data.get("first_price"), 10)
        self.assertEqual(data.get("total_price"), 60)
