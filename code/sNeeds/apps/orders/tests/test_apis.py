import json

from django.utils import timezone
import time

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.datetime_safe import datetime
from rest_framework import status, serializers
from rest_framework.test import APITestCase, APIClient

from sNeeds.apps.account.models import Country, University, FieldOfStudy
from sNeeds.apps.carts.models import Cart
from sNeeds.apps.carts.serializers import CartSerializer
from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.discounts.models import Discount, CartConsultantDiscount, TimeSlotSaleNumberDiscount
from sNeeds.apps.discounts.serializers import ConsultantDiscountSerializer
from sNeeds.apps.orders.models import Order
from sNeeds.apps.store.models import TimeSlotSale, SoldTimeSlotSale
from sNeeds.apps.store.serializers import SoldTimeSlotSaleSerializer

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

        # Carts -------
        self.cart1 = Cart.objects.create(user=self.user1)
        self.cart1.products.set([self.time_slot_sale1, self.time_slot_sale2])
        self.cart1.save()

        self.cart2 = Cart.objects.create(user=self.user1)
        self.cart2.products.set([self.time_slot_sale1, self.time_slot_sale3])

        self.cart3 = Cart.objects.create(user=self.user2)
        self.cart3.products.set([self.time_slot_sale1, self.time_slot_sale5])

        # Consultant discounts
        self.consultant_discount1 = Discount.objects.create(
            percent=10,
            code="discountcode1",
        )
        self.consultant_discount1.consultants.set([self.consultant1_profile, self.consultant2_profile])

        self.consultant_discount2 = Discount.objects.create(
            percent=20,
            code="discountcode2",
        )
        self.consultant_discount2.consultants.set([self.consultant1_profile, ])

        # Cart consultant discounts
        self.cart_consultant_discount1 = CartConsultantDiscount.objects.create(
            cart=self.cart1,
            consultant_discount=self.consultant_discount1
        )

        self.time_slot_sale_number_discount = TimeSlotSaleNumberDiscount.objects.create(
            number=2,
            discount=50
        )

        # Setup ------
        self.client = APIClient()

    def test_selling_cart_deletes_sold_products_from_other_carts(self):
        cart1_time_slot_sales = self.cart1.products.all().get_time_slot_sales()
        cart1_time_slot_sales_id = [obj.id for obj in cart1_time_slot_sales]

        cart2_time_slot_sales = self.cart2.products.all().get_time_slot_sales()
        cart2_time_slot_sales_id = [obj.id for obj in cart2_time_slot_sales]

        cart1_cart2_time_slot_sales_intersection = list(set(cart1_time_slot_sales_id) & set(cart2_time_slot_sales_id))
        if len(cart1_cart2_time_slot_sales_intersection) == 0:
            has_common_time_slot_sales = False
        else:
            has_common_time_slot_sales = True

        self.assertEqual(has_common_time_slot_sales, True)

        # Order creation
        Order.objects.sell_cart_create_order(self.cart1)

        cart2_time_slot_sales = self.cart2.products.all().get_time_slot_sales()
        cart2_time_slot_sales_id = [obj.id for obj in cart2_time_slot_sales]

        if len(list(set(cart1_cart2_time_slot_sales_intersection) & set(cart2_time_slot_sales_id))) == 0:
            has_common_time_slot_sales = False
        else:
            has_common_time_slot_sales = True

        self.assertEqual(has_common_time_slot_sales, False)

    def test_selling_cart_works(self):
        class TempTimeSlotSale:
            def __init__(self, consultant, price, start_time, end_time):
                self.consultant = consultant
                self.price = price
                self.start_time = start_time
                self.end_time = end_time

        self.cart1.refresh_from_db()

        cart1_time_slot_sales_qs = self.cart1.products.all().get_time_slot_sales()

        cart1_temp_time_slot_sales_list = []
        for obj in cart1_time_slot_sales_qs:
            cart1_temp_time_slot_sales_list.append(
                TempTimeSlotSale(obj.consultant, obj.price, obj.start_time, obj.end_time)
            )

        try:
            cart1_consultant_discount = CartConsultantDiscount.objects.get(cart=self.cart1).consultant_discount
        except CartConsultantDiscount.DoesNotExist:
            cart1_consultant_discount = None

        cart1_time_slot_sale_number_discount = TimeSlotSaleNumberDiscount.objects.get_discount_or_zero(
            self.cart1.products.all().get_time_slot_sales().count()
        )

        cart1_user = self.cart1.user
        cart1_total = self.cart1.total
        cart1_subtotal = self.cart1.subtotal

        self.cart1.refresh_from_db()
        order = Order.objects.sell_cart_create_order(self.cart1)

        order_sold_time_slot_sales = order.sold_products.all().get_sold_time_slot_sales()
        for sold_time_slot_sale in order_sold_time_slot_sales:
            self.assertEqual(
                order_sold_time_slot_sales.filter(
                    sold_to=cart1_user,
                    consultant=sold_time_slot_sale.consultant,
                    price=sold_time_slot_sale.price,
                    start_time=sold_time_slot_sale.start_time,
                    end_time=sold_time_slot_sale.end_time
                ).count(),
                1
            )

        self.assertEqual(order.user, cart1_user)
        self.assertEqual(order.status, "paid")
        self.assertEqual(order.used_consultant_discount, cart1_consultant_discount)
        self.assertEqual(order.time_slot_sales_number_discount, cart1_time_slot_sale_number_discount)
        self.assertEqual(order.total, cart1_total)
        self.assertEqual(order.subtotal, cart1_subtotal)

    def test_orders_list_get_pass(self):
        order1 = Order.objects.sell_cart_create_order(self.cart1)
        order2 = Order.objects.sell_cart_create_order(self.cart2)

        url = reverse("order:order-list", )
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            sorted([obj.get("id") for obj in response.data]),
            sorted([order1.id, order2.id])
        )

    def test_orders_list_get_pass_with_permissions(self):
        order1 = Order.objects.sell_cart_create_order(self.cart1)
        order3 = Order.objects.sell_cart_create_order(self.cart3)

        url = reverse("order:order-list", )
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            sorted([obj.get("id") for obj in response.data]),
            sorted([order1.id])
        )
        self.assertFalse(order3.id in [obj.get("id") for obj in response.data])

    def test_orders_list_get_pass_created_ordering(self):
        order1 = Order.objects.sell_cart_create_order(self.cart1)
        order2 = Order.objects.sell_cart_create_order(self.cart2)

        url = "%s?%s=%s" % (reverse("order:order-list"), "ordering", "created")

        client = self.client
        client.login(email='u1@g.com', password='user1234')

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            [obj.get("id") for obj in response.data],
            [order1.id, order2.id]
        )

    def test_orders_list_get_pass_created_ordering_descending(self):
        order1 = Order.objects.sell_cart_create_order(self.cart1)
        order2 = Order.objects.sell_cart_create_order(self.cart2)

        url = "%s?%s=%s" % (reverse("order:order-list"), "ordering", "-created")
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            [obj.get("id") for obj in response.data],
            [order2.id, order1.id]
        )

    def test_orders_detail_pass(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        order1 = Order.objects.sell_cart_create_order(self.cart1)

        url = reverse("order:order-detail", args=(order1.id,))

        response = client.get(url, format='json')
        request = response.wsgi_request
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get("id"), order1.id)
        self.assertEqual(response_data.get("order_id"), order1.order_id)
        self.assertEqual(response_data.get("status"), order1.status)
        self.assertEqual(
            response_data.get("sold_time_slot_sales"),
            SoldTimeSlotSaleSerializer(
                order1.sold_products.all().get_sold_time_slot_sales(), context={"request": request}, many=True
            ).data
        )
        self.assertEqual(
            response.data.get("created"),
            serializers.DateTimeField().to_representation(order1.created)
        )
        self.assertEqual(
            response.data.get("updated"),
            serializers.DateTimeField().to_representation(order1.updated)
        )
        self.assertEqual(
            response_data.get("used_consultant_discount"),
            {"code": order1.used_consultant_discount.code, "percent": order1.used_consultant_discount.percent}
        )
        self.assertEqual(response_data.get("time_slot_sales_number_discount"), order1.time_slot_sales_number_discount)
        self.assertEqual(response_data.get("subtotal"), order1.subtotal)
        self.assertEqual(response_data.get("total"), order1.total)

    def test_orders_detail_permission(self):
        client = self.client
        client.login(email='u2@g.com', password='user1234')

        order1 = Order.objects.sell_cart_create_order(self.cart1)

        url = reverse("order:order-detail", args=(order1.id,))
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
