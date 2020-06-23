from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.discounts.models import Discount, CartDiscount, TimeSlotSaleNumberDiscount
from sNeeds.apps.store.models import SoldProduct
from sNeeds.apps.storePackages.models import SoldStorePaidPackagePhase
from sNeeds.apps.storePackages.managers import SoldStorePaidPackagePhaseQuerySet

User = get_user_model()

ORDER_STATUS_CHOICES = (
    ('paid', 'Paid'),
    ('canceled_not_refunded', 'Canceled but not refunded'),
    ('canceled_refunded', 'Canceled and refunded'),
)


class OrderManager(models.Manager):
    # TODO Don't we save the price of product that is applied in factor after using discount ?? certainly it defers from
    # TODO primary price
    @transaction.atomic
    def sell_cart_create_order(self, cart):
        cart_products = cart.products.all()
        time_slot_sales_qs = cart_products.get_time_slot_sales()
        store_packages_qs = cart_products.get_store_packages()
        sold_store_unpaid_package_phases_qs = cart_products.get_sold_store_unpaid_package_phases()
        basic_products_qs = cart_products.get_basic_products()

        try:
            used_discount = CartDiscount.objects.get(cart=cart).discount
        except CartDiscount.DoesNotExist:
            used_discount = None

        try:
            time_slot_sales_number_discount_number = TimeSlotSaleNumberDiscount.objects.get(
                number=cart.get_time_slot_sales_count()
            ).discount
        except TimeSlotSaleNumberDiscount.DoesNotExist:
            time_slot_sales_number_discount_number = 0

        sold_time_slot_sales_qs = time_slot_sales_qs.set_time_slot_sold(sold_to=cart.user)
        # This is not SoldProduct
        sold_store_packages_qs = store_packages_qs.sell_and_get_sold_package(sold_to=cart.user)
        # This is SoldProduct
        sold_store_paid_package_phase_qs = SoldStorePaidPackagePhase.objects.filter(
            sold_store_package__in=list(sold_store_packages_qs)
        )
        sold_basic_products_qs = basic_products_qs.add_basic_product_sold(sold_to=cart.user)
        sold_store_paid_package_phases_qs = sold_store_unpaid_package_phases_qs.sell_and_get_paid_phases()

        order = Order.objects.create(
            user=cart.user,
            status='paid',
            total=cart.total,
            subtotal=cart.subtotal,
            used_discount=used_discount,
            time_slot_sales_number_discount=time_slot_sales_number_discount_number
        )

        order.sold_products.add(*list(sold_time_slot_sales_qs))
        order.sold_products.add(*list(sold_store_paid_package_phase_qs))
        order.sold_products.add(*list(sold_basic_products_qs))
        order.sold_products.add(*list(sold_store_paid_package_phases_qs))

        order.save()

        cart.delete()
        if used_discount:
            used_discount.update_decrease_use_limit()

        return order


class Order(models.Model):
    order_id = models.CharField(unique=True, max_length=12, blank=True,
                                help_text="Leave this field blank, this will populate automatically."
                                )
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    status = models.CharField(max_length=256, default='paid', choices=ORDER_STATUS_CHOICES)
    sold_products = models.ManyToManyField(SoldProduct, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # TODO:Change to code.
    used_discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    time_slot_sales_number_discount = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    subtotal = models.PositiveIntegerField()
    total = models.PositiveIntegerField()

    objects = OrderManager()

    def get_user(self):
        return self.user

    def __str__(self):
        return "Order: {} | pk: {} ".format(str(self.order_id), str(self.pk))
