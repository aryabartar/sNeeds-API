from django.utils import timezone
import time

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from sNeeds.apps.account.models import Country, University, FieldOfStudy
from sNeeds.apps.carts.models import Cart
from sNeeds.apps.carts.serializers import CartSerializer
from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.discounts.models import Discount, CartDiscount, TimeSlotSaleNumberDiscount
from sNeeds.apps.discounts.serializers import ShortDiscountSerializer
from sNeeds.apps.store.models import TimeSlotSale, SoldTimeSlotSale
from sNeeds.apps.basicProducts.models import BasicProduct
from sNeeds.apps.storePackages.models import SoldStorePackage, StorePackage, StorePackagePhase, \
    SoldStoreUnpaidPackagePhase, SoldStorePaidPackagePhase

User = get_user_model()


# from sNeeds.apps.carts.models import Cart

class DiscountTest(APITestCase):
    def setUp(self):
        # Users -------
        self.user1 = User.objects.create_user(email="u1@g.com", password="user1234")
        self.user1.is_admin = False
        self.user1.set_user_type_student()

        self.user2 = User.objects.create_user(email="u2@g.com", password="user1234")
        self.user2.is_admin = False
        self.user2.set_user_type_student()

        self.user3 = User.objects.create_user(email="u3@g.com", password="user1234")
        self.user3.is_admin = False
        self.user3.set_user_type_student()

        # Countries -------
        self.country1 = Country.objects.create(
            name="country1",
            slug="country1",
            picture=None
        )

        self.country2 = Country.objects.create(
            name="country2",
            slug="country2",
            picture=None
        )

        # Universities -------
        self.university1 = University.objects.create(
            name="university1",
            country=self.country1,
            description="Test desc1",
            picture=None,
            slug="university1"
        )

        self.university2 = University.objects.create(
            name="university2",
            country=self.country2,
            description="Test desc2",
            picture=None,
            slug="university2"
        )

        # Field of Studies -------
        self.field_of_study1 = FieldOfStudy.objects.create(
            name="field of study1",
            description="Test desc1",
            picture=None,
            slug="field-of-study1"
        )

        self.field_of_study2 = FieldOfStudy.objects.create(
            name="field of study2",
            description="Test desc2",
            picture=None,
            slug="field-of-study2"
        )

        # Consultants -------
        self.consultant1 = User.objects.create_user(email="c1@g.com", password="user1234")
        self.consultant1.is_admin = False
        self.consultant1.set_user_type_consultant()
        self.consultant1_profile = ConsultantProfile.objects.create(
            user=self.consultant1,
            bio="bio1",
            profile_picture=None,
            aparat_link="https://www.aparat.com/v/vG4QC",
            resume=None,
            slug="consultant1",
            active=True,
            time_slot_price=100
        )
        self.consultant1_profile.universities.set([self.university1, self.university2])
        self.consultant1_profile.field_of_studies.set([self.field_of_study1])
        self.consultant1_profile.countries.set([self.country1])

        self.consultant2 = User.objects.create_user(email="c2@g.com", password="user1234")
        self.consultant2.is_admin = False
        self.consultant2.set_user_type_consultant()
        self.consultant2_profile = ConsultantProfile.objects.create(
            user=self.consultant2,
            bio="bio2",
            profile_picture=None,
            aparat_link="https://www.aparat.com/v/vG4QC",
            resume=None,
            slug="consultant2",
            active=True,
            time_slot_price=80
        )

        # TimeSlotSales -------
        self.time_slot_sale1 = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(hours=1),
            end_time=timezone.now() + timezone.timedelta(hours=2),
            price=self.consultant1_profile.time_slot_price
        )
        self.time_slot_sale2 = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(hours=2),
            end_time=timezone.now() + timezone.timedelta(hours=3),
            price=self.consultant1_profile.time_slot_price
        )
        self.time_slot_sale3 = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=1, hours=1),
            price=self.consultant1_profile.time_slot_price
        )
        self.time_slot_sale4 = TimeSlotSale.objects.create(
            consultant=self.consultant2_profile,
            start_time=timezone.now() + timezone.timedelta(hours=1),
            end_time=timezone.now() + timezone.timedelta(hours=2),
            price=self.consultant2_profile.time_slot_price
        )
        self.time_slot_sale5 = TimeSlotSale.objects.create(
            consultant=self.consultant2_profile,
            start_time=timezone.now() + timezone.timedelta(hours=7),
            end_time=timezone.now() + timezone.timedelta(hours=8),
            price=self.consultant2_profile.time_slot_price
        )

        # basicProducts
        self.basic_product1 = BasicProduct.objects.create(
            title="basic_product1",
            slug="basic_product1",
            active=True,
            price=30000,
        )

        self.basic_product2 = BasicProduct.objects.create(
            title="basic_product2",
            slug="basic_product2",
            active=True,
            price=30000,
        )

        self.basic_product3 = BasicProduct.objects.create(
            title="basic_product3",
            slug="basic_product3",
            active=True,
            price=30000,
        )

        self.basic_product4 = BasicProduct.objects.create(
            title="basic_product4",
            slug="basic_product4",
            active=False,
            price=30000,
        )

        # Carts -------

        self.cart1 = Cart.objects.create(user=self.user1)
        self.cart1.products.set([self.time_slot_sale1, self.time_slot_sale2])

        self.cart2 = Cart.objects.create(user=self.user1)
        self.cart2.products.set([self.time_slot_sale1, self.time_slot_sale3])

        self.cart3 = Cart.objects.create(user=self.user2)
        self.cart3.products.set([self.time_slot_sale1, self.time_slot_sale5])

        self.cart4 = Cart.objects.create(user=self.user1)
        self.cart4.products.set([self.basic_product1])

        self.cart5 = Cart.objects.create(user=self.user1)
        self.cart5.products.set([self.basic_product2])

        self.cart6 = Cart.objects.create(user=self.user1)
        self.cart6.products.set([self.basic_product1, self.basic_product2])

        # Consultant discounts
        self.discount1 = Discount.objects.create(
            amount=10,
            code="discountcode1",
        )
        self.discount1.consultants.set([self.consultant1_profile, self.consultant2_profile])

        self.discount2 = Discount.objects.create(
            amount=20,
            code="discountcode2",
        )
        self.discount2.consultants.set([self.consultant1_profile, ])

        self.discount3 = Discount.objects.create(
            amount=500,
            code="discountcode3"
        )
        self.discount3.products.set([self.basic_product1])

        # 100 percent consultant1 discount to user1
        self.discount4 = Discount.objects.create(
            amount=self.consultant1_profile.time_slot_price,
            code="discount4",
        )
        self.discount4.consultants.set([self.consultant1_profile])
        self.discount4.users.set([self.user1])
        self.discount4.creator = "consultant"
        self.discount4.use_limit = 1
        self.discount4.save()

        self.discount5 = Discount.objects.create(
            amount=self.consultant1_profile.time_slot_price,
            code="discount5",
        )
        self.discount5.consultants.set([self.consultant1_profile])
        self.discount5.users.set([self.user2])
        self.discount5.use_limit = 1
        self.discount5.save()

        # Cart consultant discounts
        self.cart_discount1 = CartDiscount.objects.create(
            cart=self.cart1,
            discount=self.discount1
        )

        self.store_package_1 = StorePackage.objects.create(
            title="Math Gold Package",
            slug="math-gold-package"
        )

        self.store_package_phase_1 = StorePackagePhase.objects.create(
            title="General Package Phase 1",
            detailed_title="General Package Phase",
            price=100
        )
        self.store_package_1_phase_2 = StorePackagePhase.objects.create(
            title="Math Gold Package Phase 2",
            detailed_title="Math Gold Phase",
            price=200
        )
        self.store_package_1_phase_3 = StorePackagePhase.objects.create(
            title="Math Gold Package Phase 3",
            detailed_title="Math Gold Phase",
            price=400
        )
        self.store_package_2_phase_2 = StorePackagePhase.objects.create(
            title="College Package Phase 2",
            detailed_title="College Phase",
            price=200
        )

        self.sold_store_package_1 = SoldStorePackage.objects.create(
            title="Math Gold Package",
            sold_to=self.user1,
            consultant=self.consultant1_profile
        )

        self.sold_store_paid_package_phase_1 = SoldStorePaidPackagePhase.objects.create(
            title=self.store_package_phase_1.title,
            detailed_title=self.store_package_phase_1.detailed_title,
            phase_number=1,
            consultant_done=True,
            sold_store_package=self.sold_store_package_1,
            price=self.store_package_phase_1.price
        )
        self.sold_store_paid_package_phase_2 = SoldStorePaidPackagePhase.objects.create(
            title=self.store_package_1_phase_2.title,
            detailed_title=self.store_package_1_phase_2.detailed_title,
            phase_number=2,
            consultant_done=False,
            sold_store_package=self.sold_store_package_1,
            price=self.store_package_1_phase_2.price
        )

        self.sold_store_unpaid_package_phase_3 = SoldStoreUnpaidPackagePhase.objects.create(
            title=self.store_package_1_phase_3.title,
            detailed_title=self.store_package_1_phase_3.detailed_title,
            phase_number=3,
            sold_store_package=self.sold_store_package_1,
            price=self.store_package_1_phase_3.price
        )

        # Setup ------
        self.client = APIClient()

    # Test for applying 100 percent
    def test_apply_100_percent_cart_total_subtotal_correct_without_number_discount(self):
        cart = Cart.objects.create(user=self.user1)
        products = [self.time_slot_sale1, self.time_slot_sale2,
                    self.time_slot_sale4, self.time_slot_sale5,
                    self.sold_store_unpaid_package_phase_3]
        cart.products.set(products)
        cart.save()

        cart_subtotal = 0
        for p in products:
            cart_subtotal += p.price

        cart_total = cart_subtotal - self.consultant1_profile.time_slot_price

        cart_discount = CartDiscount.objects.create(cart=cart, discount=self.discount4)

        cart.refresh_from_db()

        self.discount4.refresh_from_db()

        self.assertEqual(cart.subtotal, cart_subtotal)
        self.assertEqual(cart.total, cart_total)
        self.assertEqual(self.discount4.use_limit, 0)

    # Test for applying 100 percent
    def test_delete_100_percent_cart_total_subtotal_correct_without_number_discount(self):
        cart = Cart.objects.create(user=self.user1)
        products = [self.time_slot_sale1, self.time_slot_sale2,
                    self.time_slot_sale4, self.time_slot_sale5,
                    self.sold_store_unpaid_package_phase_3]
        cart.products.set(products)
        cart.save()

        cart_subtotal = 0
        for p in products:
            cart_subtotal += p.price
        cart_total = cart_subtotal - self.consultant1_profile.time_slot_price

        cart_discount = CartDiscount.objects.create(cart=cart, discount=self.discount4)

        cart.refresh_from_db()

        self.discount4.refresh_from_db()

        self.assertEqual(cart.subtotal, cart_subtotal)
        self.assertEqual(cart.total, cart_total)
        self.assertEqual(self.discount4.use_limit, 0)

        cart_discount = CartDiscount.objects.get(pk=cart_discount.id)
        cart_discount.delete()

        cart.refresh_from_db()

        self.discount4.refresh_from_db()

        self.assertEqual(cart.subtotal, cart_subtotal)
        self.assertEqual(cart.total, cart_subtotal)
        self.assertEqual(self.discount4.use_limit, 1)

    def test_apply_100_percent_cart_total_subtotal_correct_with_number_discount(self):
        cart = Cart.objects.create(user=self.user1)

        time_slot_number_discount1 = TimeSlotSaleNumberDiscount.objects.create(number=2, discount=10)
        time_slot_number_discount2 = TimeSlotSaleNumberDiscount.objects.create(number=3, discount=15)
        time_slot_number_discount3 = TimeSlotSaleNumberDiscount.objects.create(number=4, discount=20)

        products = [self.time_slot_sale1, self.time_slot_sale2,
                    self.time_slot_sale4, self.time_slot_sale5,
                    self.sold_store_unpaid_package_phase_3]
        cart.products.set(products)
        cart.save()

        cart_subtotal = 0
        for p in products:
            cart_subtotal += p.price

        remain_time_slots_price = self.time_slot_sale2.price + self.time_slot_sale4.price + self.time_slot_sale5.price

        cart_total = cart_subtotal - self.consultant1_profile.time_slot_price
        cart_total = cart_total - (15 * remain_time_slots_price) / 100

        cart_discount = CartDiscount.objects.create(cart=cart, discount=self.discount4)

        cart.refresh_from_db()

        self.discount4.refresh_from_db()

        self.assertEqual(cart.subtotal, cart_subtotal)
        self.assertEqual(cart.total, cart_total)
        self.assertEqual(self.discount4.use_limit, 0)

    def test_delete_100_percent_cart_total_subtotal_correct_with_number_discount(self):
        cart = Cart.objects.create(user=self.user1)

        test_time_slot_number_discount1 = TimeSlotSaleNumberDiscount.objects.create(number=2, discount=10)
        test_time_slot_number_discount2 = TimeSlotSaleNumberDiscount.objects.create(number=3, discount=15)
        test_time_slot_number_discount3 = TimeSlotSaleNumberDiscount.objects.create(number=4, discount=20)

        products = [self.time_slot_sale1, self.time_slot_sale2,
                    self.time_slot_sale4, self.time_slot_sale5,
                    self.sold_store_unpaid_package_phase_3]
        cart.products.set(products)
        cart.save()

        cart_subtotal = 0
        for p in products:
            cart_subtotal += p.price

        cart_total = cart_subtotal - self.consultant1_profile.time_slot_price

        remain_time_slots_price = self.time_slot_sale2.price + self.time_slot_sale4.price + self.time_slot_sale5.price
        cart_total = cart_total - (15 * remain_time_slots_price) / 100

        cart_discount = CartDiscount.objects.create(cart=cart, discount=self.discount4)

        cart.refresh_from_db()

        self.discount4.refresh_from_db()

        self.assertEqual(cart.subtotal, cart_subtotal)
        self.assertEqual(cart.total, cart_total)
        self.assertEqual(self.discount4.use_limit, 0)

        cart_discount = CartDiscount.objects.get(pk=cart_discount.id)
        cart_discount.delete()

        remain_time_slots_price2 = self.time_slot_sale2.price + self.time_slot_sale4.price + self.time_slot_sale5.price
        remain_time_slots_price2 += self.time_slot_sale1.price

        cart_total = cart_subtotal - (20 * remain_time_slots_price2) / 100

        cart.refresh_from_db()

        self.discount4.refresh_from_db()

        self.assertEqual(cart.subtotal, cart_subtotal)
        self.assertEqual(cart.total, cart_total)
        self.assertEqual(self.discount4.use_limit, 1)
