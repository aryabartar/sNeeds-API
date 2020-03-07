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

    def test_store_package_price_correct(self):
        self.assertEqual(self.store_package1.price, 10)

    def test_store_package_price_update_correct(self):
        self.store_package_phase_1.price = 11
        self.store_package_phase_1.save()

        self.store_package1.refresh_from_db()
        self.assertEqual(self.store_package1.price, 11)

        self.store_package_phase_through1.phase_number = 4
        self.store_package_phase_through1.save()
        self.store_package_phase_through3.phase_number = 1
        self.store_package_phase_through3.save()

        self.store_package1.refresh_from_db()
        self.assertEqual(self.store_package1.price, 30)
