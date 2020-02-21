from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.store.models import SoldProduct

User = get_user_model()

ORDER_STATUS_CHOICES = (
    ('paid', 'Paid'),
    ('canceled_not_refunded', 'Canceled but not refunded'),
    ('canceled_refunded', 'Canceled and refunded'),
)


class OrderManager(models.Manager):
    @transaction.atomic
    def sell_cart_create_order(self, cart):
        cart_products = cart.products.all()
        time_slot_sales_qs = cart_products.objects.get_time_slot_sales()
        sold_time_slot_sales_qs = time_slot_sales_qs.objects.set_time_slot_sold()

        order = Order(
            status='paid',
            total=cart.total,
            subtotal=cart.subtotal
        )
        order.sold_products.set(sold_time_slot_sales_qs)
        order.save()
        return order


class Order(models.Model):
    order_id = models.CharField(max_length=12, blank=True,
                                help_text="Leave this field blank, this will populate automatically.")
    status = models.CharField(max_length=256, default='paid', choices=ORDER_STATUS_CHOICES)
    sold_products = models.ManyToManyField(SoldProduct, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    objects = OrderManager()

    def get_user(self):
        return self.cart.user

    def __str__(self):
        return "Order: {} | pk: {} ".format(str(self.order_id), str(self.pk))
