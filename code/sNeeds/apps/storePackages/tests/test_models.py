from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from sNeeds.utils.custom.TestClasses import CustomAPITestCase
from sNeeds.apps.storePackages.models import (
    StorePackage, StorePackagePhase, StorePackagePhaseThrough, SoldStorePackage,
    SoldStoreUnpaidPackagePhase, SoldStorePaidPackagePhase
)


class TestStorePackageModels(CustomAPITestCase):

    def test_store_package_price_correct(self):
        self.assertEqual(self.store_package_1.price, 100)
        self.assertEqual(self.store_package_1.total_price, 700)

    def test_store_package_price_correct_after_add_phase(self):
        StorePackagePhaseThrough.objects.create(
            store_package=self.store_package_1,
            store_package_phase=self.store_package_2_phase_2,
            phase_number=4
        )
        self.assertEqual(self.store_package_1.price, 100)
        self.assertEqual(self.store_package_1.total_price, 900)

    def test_store_package_price_correct_after_remove_phase(self):
        self.store_package_1_phase_through_3.delete()
        self.assertEqual(self.store_package_1.price, 100)
        self.assertEqual(self.store_package_1.total_price, 300)

    def test_store_package_price_correct_after_update_phase_price(self):
        self.store_package_phase_1.price = 200
        self.store_package_phase_1.save()
        self.store_package_1_phase_2.price = 300
        self.store_package_1_phase_2.save()
        self.store_package_1.refresh_from_db()
        self.assertEqual(self.store_package_1.price, 200)
        self.assertEqual(self.store_package_1.total_price, 900)

    # def test_selling_store_package_correct(self):


    # def test_store_package_price_correct_after_add_phase(self):
    #     self.store_package_1.store_package_phases.add(self.store_package_2_phase_2)
    #     self.assertEqual(self.store_package_1.price, 100)
    #     self.assertEqual(self.store_package_1.total_price, 900)

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
