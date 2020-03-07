from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse

from sNeeds.utils.custom.TestClasses import CustomAPITestCase
from sNeeds.apps.storePackages.models import StorePackage, StorePackagePhaseThrough, StorePackagePhase


class TestStorePackage(CustomAPITestCase):

    def setUp(self):
        super().setUp()

        self.store_package_phase_1 = StorePackagePhase.objects.create(
            title="store-package-title1",
            detailed_title="detailed_store-package-title1",
            price=10
        )
        self.store_package_phase_2 = StorePackagePhase.objects.create(
            title="store-package-title2",
            detailed_title="detailed_store-package-title2",
            price=20
        )
        self.store_package_phase_3 = StorePackagePhase.objects.create(
            title="store-package-title3",
            detailed_title="detailed_store-package-title3",
            price=30
        )
        self.store_package_phase_4 = StorePackagePhase.objects.create(
            title="store-package-title4",
            detailed_title="detailed_store-package-title4",
            price=40
        )

        self.store_package1 = StorePackage.objects.create(
            title="store_package_title1",
            slug="store_package_slug1"
        )
        self.store_package2 = StorePackage.objects.create(
            title="store_package_title2",
            slug="store_package_slug2"
        )

        self.store_package_phase_through1 = StorePackagePhaseThrough.objects.create(
            store_package=self.store_package1,
            store_package_phase=self.store_package_phase_1,
            phase_number=1
        )
        self.store_package_phase_through2 = StorePackagePhaseThrough.objects.create(
            store_package=self.store_package1,
            store_package_phase=self.store_package_phase_2,
            phase_number=2
        )
        self.store_package_phase_through3 = StorePackagePhaseThrough.objects.create(
            store_package=self.store_package1,
            store_package_phase=self.store_package_phase_3,
            phase_number=3
        )
        self.store_package_phase_through4 = StorePackagePhaseThrough.objects.create(
            store_package=self.store_package2,
            store_package_phase=self.store_package_phase_2,
            phase_number=1
        )
        self.store_package_phase_through5 = StorePackagePhaseThrough.objects.create(
            store_package=self.store_package2,
            store_package_phase=self.store_package_phase_3,
            phase_number=2
        )
        self.store_package_phase_through6 = StorePackagePhaseThrough.objects.create(
            store_package=self.store_package2,
            store_package_phase=self.store_package_phase_4,
            phase_number=3
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
        self.assertEqual(data.get("title"), obj.store_package.title)
        self.assertEqual(data.get("store_package"), obj.store_package.id)
        self.assertEqual(data.get("phase_number"), obj.phase_number)
        self.assertEqual(data.get("price"), obj.store_package.price)
