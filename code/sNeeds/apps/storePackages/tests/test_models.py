# from sNeeds.utils.custom.TestClasses import CustomAPITestCase
#
#
# class TestStorePackage(CustomAPITestCase):
#
#     def setUp(self):
#         super().setUp()
#
#     def test_store_package_price_correct(self):
#         self.assertEqual(self.store_package1.price, 10)
#
#     def test_store_package_price_update_correct(self):
#         self.store_package_phase_1.price = 11
#         self.store_package_phase_1.save()
#
#         self.store_package1.refresh_from_db()
#         self.assertEqual(self.store_package1.price, 11)
#
#         self.store_package_phase_through1.phase_number = 4
#         self.store_package_phase_through1.save()
#         self.store_package_phase_through3.phase_number = 1
#         self.store_package_phase_through3.save()
#
#         self.store_package1.refresh_from_db()
#         self.assertEqual(self.store_package1.price, 30)
