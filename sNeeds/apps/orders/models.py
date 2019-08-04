from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction

from sNeeds.apps.carts.models import Cart, SoldCart

User = get_user_model()

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
)
SOLD_ORDER_STATUS_CHOICES = (
    ('paid', 'Paid'),
    ('canceled_not_refunded', 'Canceled but not refunded'),
    ('canceled_refunded', 'Canceled and refunded'),
)


class SoldOrderManager(models.Manager):
    @transaction.atomic
    def sell_order(self, order):
        cart = order.cart
        print("0")
        sold_order = SoldOrder(
            cart=None,
            status="paid",
            order_id=order.order_id,
            total=order.total,
        )
        print("a")
        cart = Cart.objects.set_cart_paid(cart)
        print("b")
        sold_order.cart = cart
        print("c")
        sold_order.save()
        print("d")
        order.delete()

        return sold_order


class AbstractOrder(models.Model):
    order_id = models.CharField(max_length=12, blank=True, help_text="Leave this field blank.")
    total = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Order: {} | pk: {} ".format(str(self.order_id), str(self.pk))

    class Meta:
        abstract = True


class Order(AbstractOrder):
    cart = models.OneToOneField(Cart, null=True, on_delete=models.CASCADE, related_name="cart_order")
    status = models.CharField(max_length=256, default='created', choices=ORDER_STATUS_CHOICES)

    def is_acceptable_for_pay(self):
        if self.total > 0:
            return True
        return False

    def update_total(self):
        self.total = self.cart.total
        self.save()
        return self.total

    def get_user(self):
        return self.cart.user


class SoldOrder(AbstractOrder):
    cart = models.OneToOneField(SoldCart, null=True, on_delete=models.SET_NULL, related_name="cart_order")
    status = models.CharField(max_length=256, default='paid', choices=SOLD_ORDER_STATUS_CHOICES)

    objects = SoldOrderManager()

    def update_total(self):
        self.total = self.cart.total
        self.save()
        return self.total

    def get_user(self):
        return self.cart.user
