from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse

from sNeeds.utils.custom.TestClasses import CustomAPITestCase
from sNeeds.apps.storePackages.models import (
    StorePackage, StorePackagePhase, StorePackagePhaseThrough, SoldStorePackage,
    SoldStoreUnpaidPackagePhase, SoldStorePaidPackagePhase
)


class TestStorePackageModels(CustomAPITestCase):

    def test_store_package_price_correct(self):
        self.assertEqual(self.store_package_1.price, 100)
        self.assertEqual(self.store_package_1.total_price, 700)
    #
    # def test_store_package_price_update_correct(self):
    #     self.store_package_phase_1.price = 11
    #     self.store_package_phase_1.save()
    #
    #     self.store_package1.refresh_from_db()
    #     self.assertEqual(self.store_package1.price, 11)
    #
    #     self.store_package_phase_through1.phase_number = 4
    #     self.store_package_phase_through1.save()
    #     self.store_package_phase_through3.phase_number = 1
    #     self.store_package_phase_through3.save()
    #
    #     self.store_package1.refresh_from_db()
    #     self.assertEqual(self.store_package1.price, 30)
