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

    def test_store_package_selling_works_correct(self):
        store_package = self.store_package_1
        qs = StorePackage.objects.filter(id=store_package.id)
        sold_store_package = qs.sell_and_get_sold_package(self.user2).first()

        self.assertEqual(sold_store_package.title, store_package.title)
        self.assertEqual(sold_store_package.sold_to, self.user2)
        self.assertEqual(sold_store_package.consultant, None)
        self.assertEqual(sold_store_package.paid_price, store_package.price)
        self.assertEqual(sold_store_package.total_price, store_package.total_price)

        sold_store_paid_package_phase_1 = SoldStorePaidPackagePhase.objects.get(
            sold_store_package=sold_store_package,
            phase_number=1
        )
        self.assertEqual(sold_store_paid_package_phase_1.title, self.store_package_phase_1.title)
        self.assertEqual(sold_store_paid_package_phase_1.detailed_title, self.store_package_phase_1.detailed_title)
        self.assertEqual(sold_store_paid_package_phase_1.sold_store_package, sold_store_package)
        self.assertEqual(sold_store_paid_package_phase_1.phase_number, 1)
        self.assertEqual(sold_store_paid_package_phase_1.sold_store_package, sold_store_package)
        self.assertEqual(sold_store_paid_package_phase_1.status, "in_progress")
        self.assertEqual(sold_store_paid_package_phase_1.consultant_done, False)
        self.assertEqual(sold_store_paid_package_phase_1.price, self.store_package_phase_1.price)
        self.assertEqual(sold_store_paid_package_phase_1.sold_to, self.user2)

        sold_store_unpaid_package_phase_2 = SoldStoreUnpaidPackagePhase.objects.get(
            sold_store_package=sold_store_package,
            phase_number=2
        )
        self.assertEqual(
            sold_store_unpaid_package_phase_2.title, self.store_package_1_phase_through_2.store_package_phase.title
        )
        self.assertEqual(
            sold_store_unpaid_package_phase_2.detailed_title,
            self.store_package_1_phase_through_2.store_package_phase.detailed_title
        )
        self.assertEqual(sold_store_unpaid_package_phase_2.sold_store_package, sold_store_package)
        self.assertEqual(sold_store_unpaid_package_phase_2.phase_number, 2)
        self.assertEqual(sold_store_unpaid_package_phase_2.status, "pay_to_start")
        self.assertEqual(
            sold_store_unpaid_package_phase_2.price, self.store_package_1_phase_through_2.store_package_phase.price
        )
        self.assertEqual(sold_store_unpaid_package_phase_2.active, True)

        sold_store_unpaid_package_phase_3 = SoldStoreUnpaidPackagePhase.objects.get(
            sold_store_package=sold_store_package,
            phase_number=3
        )
        self.assertEqual(
            sold_store_unpaid_package_phase_3.title, self.store_package_1_phase_through_3.store_package_phase.title
        )
        self.assertEqual(
            sold_store_unpaid_package_phase_3.detailed_title,
            self.store_package_1_phase_through_3.store_package_phase.detailed_title
        )
        self.assertEqual(sold_store_unpaid_package_phase_3.sold_store_package, sold_store_package)
        self.assertEqual(sold_store_unpaid_package_phase_3.phase_number, 3)
        self.assertEqual(sold_store_unpaid_package_phase_3.status, "not_started")
        self.assertEqual(
            sold_store_unpaid_package_phase_3.price, self.store_package_1_phase_through_3.store_package_phase.price
        )
        self.assertEqual(sold_store_unpaid_package_phase_3.active, False)
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
