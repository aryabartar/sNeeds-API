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

class CartTests(APITestCase):
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
            title="Math Gold Package Here Here Here",
            sold_to=self.user1,
            consultant=self.consultant1_profile,
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

    def test_cart_discounts_list_number(self):
        CartDiscount.objects.create(
            cart=self.cart3,
            discount=self.discount2
        )

        url = reverse("discount:cart-discount-list")
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        response = client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("cart"), self.cart1.id)

    def test_cart_discounts_list_get_query_parameter(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        CartDiscount.objects.create(
            cart=self.cart2,
            discount=self.discount2
        )
        # Test 1
        url = reverse("discount:cart-discount-list")
        response = client.get(url, {}, format='json')
        self.assertEqual(len(response.data), 2)

        # Test 2
        url = "%s?%s=%i" % (
            reverse("discount:cart-discount-list"), "cart", self.cart_discount1.cart.id)
        response = client.get(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("cart"), self.cart1.id)

    def test_cart_discounts_list_get_query_parameter_permission(self):
        client = self.client
        client.login(email='u2@g.com', password='user1234')

        url = "%s?%s=%s" % (
            reverse("discount:cart-discount-list"), "cart", str(self.cart_discount1.cart.id))
        response = client.get(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_cart_discount_post(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        url = reverse("discount:cart-discount-list")
        post_data = {
            "cart": self.cart2.id,
            "code": self.discount1.code
        }
        response = client.post(url, post_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['cart'], self.cart2.id)
        self.assertEqual(response.data['code'], self.discount1.code)
        self.assertDictEqual(response.data['discount'],
                             ShortDiscountSerializer(self.discount1).data)

    def test_cart_discount_post_fail_unauthorized(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        url = reverse("discount:cart-discount-list")
        post_data = {
            "cart": self.cart3.id,
            "code": self.discount1.code
        }
        response = client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cart_discount_post_fail_more_than_one_discount_on_one_cart(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        url = reverse("discount:cart-discount-list")
        post_data = {
            "cart": self.cart1.id,
            "code": self.discount2.code
        }
        response = client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cart_discount_post_fail_no_relevant_product_in_cart(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        temp_cart = Cart.objects.create(user=self.user1)
        temp_cart.products.set([self.time_slot_sale1, self.time_slot_sale2])

        temp_discount = Discount.objects.create(
            amount=20,
            code="temp_discount",
        )
        temp_discount.consultants.set([self.consultant2_profile])

        url = reverse("discount:cart-discount-list")
        post_data = {
            "cart": temp_cart.id,
            "code": temp_discount.code
        }

        response = client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cart_discount_correct_total_subtotal_update_1(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        temp_cart = Cart.objects.create(user=self.user1)
        temp_cart.products.set([self.time_slot_sale1, self.time_slot_sale2])

        temp_discount = Discount.objects.create(
            amount=20,
            code="temp_discount",
        )
        temp_discount.consultants.set([self.consultant1_profile, self.consultant2_profile])

        url = reverse("discount:cart-discount-list")
        post_data = {
            "cart": temp_cart.id,
            "code": temp_discount.code
        }

        response = client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse("cart:cart-detail", args=(temp_cart.id,))
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("total"), 160)
        self.assertEqual(response.data.get("subtotal"), 200)

    def test_cart_discount_correct_total_subtotal_update_2(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        temp_cart = Cart.objects.create(user=self.user1)
        temp_cart.products.set([self.time_slot_sale1, self.time_slot_sale4])

        temp_discount = Discount.objects.create(
            amount=20,
            code="temp_discount",
        )
        temp_discount.consultants.set([self.consultant1_profile, ])

        url = reverse("discount:cart-discount-list")
        post_data = {
            "cart": temp_cart.id,
            "code": temp_discount.code
        }

        response = client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse("cart:cart-detail", args=(temp_cart.id,))
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("total"), 160)
        self.assertEqual(response.data.get("subtotal"), 180)

    def test_cart_discount_detail_get(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        url = reverse("discount:cart-discount-detail", args=(self.cart_discount1.id,))
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("cart"), self.cart_discount1.cart.id)

    def test_cart_discount_detail_get_no_permission(self):
        client = self.client
        client.login(email='u2@g.com', password='user1234')

        url = reverse("discount:cart-discount-detail", args=(self.cart_discount1.id,))
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cart_discount_detail_get_unauthorized(self):
        client = self.client

        url = reverse("discount:cart-discount-detail", args=(self.cart_discount1.id,))
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cart_discount_detail_delete(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        url = reverse("discount:cart-discount-detail", args=(self.cart_discount1.id,))
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cart_discount_detail_delete_no_permission(self):
        client = self.client
        client.login(email='u2@g.com', password='user1234')

        url = reverse("discount:cart-discount-detail", args=(self.cart_discount1.id,))
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cart_discount_detail_delete_unauthorized(self):
        client = self.client

        url = reverse("discount:cart-discount-detail", args=(self.cart_discount1.id,))
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cart_discount_delete_updates_cart_total_subtotal(self):
        self.assertEqual(self.cart1.total, 180)
        self.assertEqual(self.cart1.subtotal, 200)
        self.cart_discount1.delete()
        self.assertEqual(self.cart1.total, 200)
        self.assertEqual(self.cart1.total, 200)

    def test_time_slot_sale_number_discount_correct_cart_total_subtotal(self):
        self.assertEqual(self.cart1.total, 180)
        self.assertEqual(self.cart1.subtotal, 200)

        time_slot_sale_number_discount_1 = TimeSlotSaleNumberDiscount.objects.create(
            number=2,
            discount=50
        )

        # self.cart was not updating!
        self.assertEqual(Cart.objects.get(id=self.cart1.id).total, 90)
        self.assertEqual(Cart.objects.get(id=self.cart1.id).subtotal, 200)

        time_slot_sale_number_discount_1.delete()

        # self.cart was not updating!
        self.assertEqual(Cart.objects.get(id=self.cart1.id).total, 180)
        self.assertEqual(Cart.objects.get(id=self.cart1.id).subtotal, 200)

    def test_list_consultant_discounts_time_slot_interact_post_success(self):
        url = reverse("discount:consultant-discount-list")

        client = self.client
        client.force_login(self.consultant2)

        SoldTimeSlotSale.objects.create(consultant=self.consultant2_profile, sold_to=self.user2,
                                        price=5000, start_time=timezone.now() + timezone.timedelta(hours=1),
                                        end_time=timezone.now() + timezone.timedelta(hours=3))
        users = [self.user2]
        payload = {
            "users": [i.id for i in users]
        }

        response = client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get('code', None))
        self.assertEqual(len(response.data.get('products')), 0)
        self.assertEqual(response.data.get('users').pop(), self.user2.id)
        self.assertEqual(response.data.get('consultants').pop(), self.consultant2_profile.id)
        self.assertEqual(response.data.get('amount'), self.consultant2_profile.time_slot_price)
        discount_id = response.data.get('id')
        discount = Discount.objects.get(pk=discount_id)
        self.assertEqual(discount.use_limit, 1)

    def test_list_consultant_discounts_store_package_interact_post_success(self):
        url = reverse("discount:consultant-discount-list")

        client = self.client
        client.force_login(self.consultant2)

        SoldStoreUnpaidPackagePhase.objects.get(pk=self.sold_store_unpaid_package_phase_3.id).delete()
        SoldStorePaidPackagePhase.objects.get(pk=self.sold_store_paid_package_phase_2.id).delete()
        SoldStorePaidPackagePhase.objects.get(pk=self.sold_store_paid_package_phase_1.id).delete()
        SoldStorePackage.objects.get(pk=self.sold_store_package_1.id).delete()

        SoldStorePackage.objects.create(consultant=self.consultant2_profile, sold_to=self.user2,
                                        paid_price=5000, total_price=15000, title="Hello")
        users = [self.user2]
        payload = {
            "users": [i.id for i in users]
        }

        response = client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get('code', None))
        self.assertEqual(len(response.data.get('products')), 0)
        self.assertEqual(response.data.get('users').pop(), self.user2.id)
        self.assertEqual(response.data.get('consultants').pop(), self.consultant2_profile.id)
        self.assertEqual(response.data.get('amount'), self.consultant2_profile.time_slot_price)
        discount_id = response.data.get('id')
        discount = Discount.objects.get(pk=discount_id)
        self.assertEqual(discount.use_limit, 1)

    def test_list_consultant_discount_users_no_interacts_post_fail(self):
        url = reverse("discount:consultant-discount-list")
        client = self.client
        client.force_login(self.consultant2)

        SoldStoreUnpaidPackagePhase.objects.get(pk=self.sold_store_unpaid_package_phase_3.id).delete()
        SoldStorePaidPackagePhase.objects.get(pk=self.sold_store_paid_package_phase_2.id).delete()
        SoldStorePaidPackagePhase.objects.get(pk=self.sold_store_paid_package_phase_1.id).delete()
        SoldStorePackage.objects.get(pk=self.sold_store_package_1.id).delete()

        SoldStorePackage.objects.create(consultant=self.consultant2_profile, sold_to=self.user1,
                                        paid_price=5000, total_price=15000, title="Hello")
        users = [self.user2]
        payload = {
            "users": [i.id for i in users]
        }

        response = client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_consultant_discount_non_consultant_access_fail_forbidden(self):
        url = reverse("discount:consultant-discount-list")
        client = self.client
        client.force_login(self.user2)
        users = [self.user2]
        payload = {
            "users": [i.id for i in users]
        }

        response = client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_consultant_discount_unauthorized_fail(self):
        url = reverse("discount:consultant-discount-list")
        client = self.client
        users = [self.user2]
        payload = {
            "users": [i.id for i in users]
        }

        response = client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_consultant_discount_more_than_1_user_post_fail(self):
        url = reverse("discount:consultant-discount-list")
        client = self.client
        client.force_login(self.consultant2)
        users = [self.user2, self.user1]
        payload = {
            "users": [i.id for i in users]
        }

        response = client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_consultant_discount_consultant_in_users_post_fail(self):
        url = reverse("discount:consultant-discount-list")
        client = self.client
        client.force_login(self.consultant2)
        users = [self.consultant1]
        payload = {
            "users": [i.id for i in users]
        }

        response = client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_detail_consultant_discount_get_success(self):
        url = reverse("discount:consultant-discount-detail", args=(self.discount4.id,))
        client = self.client
        client.force_login(self.consultant1)

        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('users').pop(), self.user1.id)

    def test_detail_consultant_discount_delete_success(self):
        url = reverse("discount:consultant-discount-detail", args=(self.discount4.id,))
        client = self.client
        client.force_login(self.consultant1)

        discount_id = self.discount4.id

        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Discount.objects.filter(pk=discount_id).exists(), False)

    def test_detail_consultant_discount_put_patch_fail(self):
        url = reverse("discount:consultant-discount-detail", args=(self.discount4.id,))
        client = self.client
        client.force_login(self.consultant1)

        users = [self.user2]
        payload = {
            "users": [i.id for i in users]
        }

        response = client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_detail_consultant_discount_get_delete_not_owner_consultant_fail(self):
        url = reverse("discount:consultant-discount-detail", args=(self.discount4.id,))
        client = self.client
        client.force_login(self.consultant2)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_consultant_discount_put_patch_not_owner_consultant_fail(self):
        url = reverse("discount:consultant-discount-detail", args=(self.discount4.id,))
        client = self.client
        client.force_login(self.consultant2)

        users = [self.user2]
        payload = {
            "users": [i.id for i in users]
        }
        response = client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_detail_consultant_discount_get_user_not_owner_non_consultant_but_in_users_fail(self):
        url = reverse("discount:consultant-discount-detail", args=(self.discount4.id,))
        client = self.client
        client.force_login(self.user1)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_consultant_discount_delete_user_not_owner_non_consultant_but_in_users_fail(self):
        url = reverse("discount:consultant-discount-detail", args=(self.discount4.id,))
        client = self.client
        client.force_login(self.user1)

        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_consultant_discount_put_patch_user_not_owner_non_consultant_but_in_users_fail(self):
        url = reverse("discount:consultant-discount-detail", args=(self.discount4.id,))
        client = self.client
        client.force_login(self.user1)

        users = [self.user1]
        payload = {
            "users": [i.id for i in users]
        }

        response = client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_consultant_discount_access_user_not_owner_not_consultant_not_in_users_fail(self):
        url = reverse("discount:consultant-discount-detail", args=(self.discount4.id,))
        client = self.client
        client.force_login(self.user2)

        users = [self.user2]
        payload = {
            "users": [i.id for i in users]
        }

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Tests for get suitable users for give discount by consultant
    def test_list_consultant_interact_user_get_success(self):
        url = reverse('discount:consultant-interact-user-list')

        SoldStoreUnpaidPackagePhase.objects.get(pk=self.sold_store_unpaid_package_phase_3.id).delete()
        SoldStorePaidPackagePhase.objects.get(pk=self.sold_store_paid_package_phase_2.id).delete()
        SoldStorePaidPackagePhase.objects.get(pk=self.sold_store_paid_package_phase_1.id).delete()
        SoldStorePackage.objects.get(pk=self.sold_store_package_1.id).delete()

        SoldTimeSlotSale.objects.create(consultant=self.consultant1_profile, sold_to=self.user1,
                                        price=5000, start_time=timezone.now() + timezone.timedelta(hours=1),
                                        end_time=timezone.now() + timezone.timedelta(hours=3))

        SoldTimeSlotSale.objects.create(consultant=self.consultant1_profile, sold_to=self.user2,
                                        price=5000, start_time=timezone.now() + timezone.timedelta(hours=10),
                                        end_time=timezone.now() + timezone.timedelta(hours=12))

        SoldStorePackage.objects.create(consultant=self.consultant1_profile, sold_to=self.user2,
                                        paid_price=5000, total_price=15000, title="Hello")

        SoldStorePackage.objects.create(consultant=self.consultant2_profile, sold_to=self.user3,
                                        paid_price=5000, total_price=15000, title="Hello")

        SoldTimeSlotSale.objects.create(consultant=self.consultant2_profile, sold_to=self.user3,
                                        price=5000, start_time=timezone.now() + timezone.timedelta(hours=10),
                                        end_time=timezone.now() + timezone.timedelta(hours=12))

        client = self.client
        client.force_login(self.consultant1)

        response = client.get(url)

        # print(response.data)
        self.assertEqual(response.data.get('consultant').get('id'), self.consultant1_profile.id)
        self.assertEqual(len(response.data.get('interact_users', [])), 2)
        interact_users = []
        for user in response.data.get('interact_users', []):
            interact_users.append(user.get('id'))

        self.assertTrue(self.user1.id in interact_users)
        self.assertTrue(self.user2.id in interact_users)
        self.assertFalse(self.user3.id in interact_users)

    def test_list_consultant_interact_user_zero_sold_zero_user(self):

        SoldStoreUnpaidPackagePhase.objects.get(pk=self.sold_store_unpaid_package_phase_3.id).delete()
        SoldStorePaidPackagePhase.objects.get(pk=self.sold_store_paid_package_phase_2.id).delete()
        SoldStorePaidPackagePhase.objects.get(pk=self.sold_store_paid_package_phase_1.id).delete()
        SoldStorePackage.objects.get(pk=self.sold_store_package_1.id).delete()

        url = reverse('discount:consultant-interact-user-list')

        client = self.client
        client.force_login(self.consultant1)

        response = client.get(url)

        self.assertEqual(response.data.get('consultant').get('id'), self.consultant1_profile.id)

        self.assertEqual(len(response.data.get('interact_users', [])), 0)

    def test_list_consultant_interact_post_put_patch_delete_fail(self):
        url = reverse('discount:consultant-interact-user-list')

        SoldTimeSlotSale.objects.create(consultant=self.consultant1_profile, sold_to=self.user2,
                                        price=5000, start_time=timezone.now() + timezone.timedelta(hours=10),
                                        end_time=timezone.now() + timezone.timedelta(hours=12))

        SoldStorePackage.objects.create(consultant=self.consultant1_profile, sold_to=self.user2,
                                        paid_price=5000, total_price=15000, title="Hello")

        client = self.client
        client.force_login(self.consultant1)

        payload = {'consultant': {'id': 2, 'first_name': "ALi"}, }

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_consultant_interact_access_denied_unauthorized(self):
        url = reverse('discount:consultant-interact-user-list')

        SoldTimeSlotSale.objects.create(consultant=self.consultant1_profile, sold_to=self.user2,
                                        price=5000, start_time=timezone.now() + timezone.timedelta(hours=10),
                                        end_time=timezone.now() + timezone.timedelta(hours=12))

        SoldStorePackage.objects.create(consultant=self.consultant1_profile, sold_to=self.user2,
                                        paid_price=5000, total_price=15000, title="Hello")

        client = self.client

        payload = {'consultant': {'id': 2, 'first_name': "ALi"}, }

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_consultant_interact_non_consultant_user_access_denied(self):
        url = reverse('discount:consultant-interact-user-list')

        SoldTimeSlotSale.objects.create(consultant=self.consultant1_profile, sold_to=self.user2,
                                        price=5000, start_time=timezone.now() + timezone.timedelta(hours=10),
                                        end_time=timezone.now() + timezone.timedelta(hours=12))

        SoldStorePackage.objects.create(consultant=self.consultant1_profile, sold_to=self.user2,
                                        paid_price=5000, total_price=15000, title="Hello")

        client = self.client
        client.force_login(self.user1)

        payload = {'consultant': {'id': 2, 'first_name': "ALi"}, }

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_apply_100_percent_cart_total_subtotal_correct_without_number_discount(self):
        url = reverse('discount:cart-discount-list')
        client = self.client
        client.force_login(self.user1)

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

        payload = {
            'cart': cart.id,
            'code': self.discount4.code
        }

        response = client.post(url, payload, format='json')

        self.discount4.refresh_from_db()
        cart = Cart.objects.get(pk=response.data['cart'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(cart.subtotal, cart_subtotal)
        self.assertEqual(cart.total, cart_total)
        self.assertEqual(self.discount4.use_limit, 0)

    def test_delete_100_percent_cart_total_subtotal_correct_without_number_discount(self):

        client = self.client
        client.force_login(self.user1)

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

        url = reverse('discount:cart-discount-detail', args=(cart_discount.id,))
        response = client.get(url)
        cart = Cart.objects.get(pk=response.data['cart'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cart.subtotal, cart_subtotal)
        self.assertEqual(cart.total, cart_total)

        response = client.delete(url, format='json')

        self.discount4.refresh_from_db()
        cart.refresh_from_db()
        cart_total = cart_subtotal

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(cart.subtotal, cart_subtotal)
        self.assertEqual(cart.total, cart_total)

    def test_list_cart_discount_100_percent_user_no_in_users_fail(self):
        url = reverse('discount:cart-discount-list')
        client = self.client
        client.force_login(self.user2)

        cart = Cart.objects.create(user=self.user2)
        products = [self.time_slot_sale1, self.time_slot_sale2,
                    self.time_slot_sale4, self.time_slot_sale5,
                    self.sold_store_unpaid_package_phase_3]
        cart.products.set(products)
        cart.save()
        cart_subtotal = 0
        for p in products:
            cart_subtotal += p.price
        cart_total = cart_subtotal

        payload = {
            'cart': cart.id,
            'code': self.discount4.code
        }

        response = client.post(url, payload, format='json')

        self.discount4.refresh_from_db()
        cart.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(cart.subtotal, cart_subtotal)
        self.assertEqual(cart.total, cart_total)
        self.assertEqual(self.discount4.use_limit, 1)









