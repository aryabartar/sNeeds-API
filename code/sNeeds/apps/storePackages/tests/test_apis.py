from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from sNeeds.utils.custom.TestClasses import CustomAPITestCase
from sNeeds.apps.storePackages.models import (
    StorePackage, StorePackagePhase, StorePackagePhaseThrough, SoldStorePackage,
    SoldStoreUnpaidPackagePhase, SoldStorePaidPackagePhase
)


class TestAPIStorePackage(CustomAPITestCase):

    def test_store_package_phase_through_list_get_success(self):
        client = self.client
        url = reverse("store-package:store-package-phase-through-list")

        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_store_package_phase_through_detail_get_success(self):
        client = self.client
        url = reverse(
            "store-package:store-package-phase-through-detail",
            args=[self.store_package_1_phase_through_1.id]
        )

        response = client.get(url, format="json")

        data = response.data
        obj = self.store_package_1_phase_through_1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("id"), obj.id)
        self.assertEqual(data.get("title"), obj.store_package_phase.title)
        self.assertNotEqual(data.get("store_package"), None)
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
        url = reverse(
            "store-package:store-package-detail",
            args=[self.store_package_1.slug, ]
        )

        response = client.get(url, format="json")

        data = response.data
        obj = self.store_package_1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), obj.title)
        self.assertEqual(data.get("active"), obj.active)
        self.assertEqual(len(data.get("store_package_phases")), len(obj.store_package_phases.all()))
        self.assertEqual(data.get("price"), obj.price)
        self.assertEqual(data.get("total_price"), obj.total_price)
