from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save, post_save

from .utils import unique_order_id_generator

from sNeeds.apps.carts.models import Cart, SoldCart

User = get_user_model()

SOLD_ORDER_STATUS_CHOICES = (
    ('paid', 'Paid'),
    ('canceled_not_refunded', 'Canceled but not refunded'),
    ('canceled_refunded', 'Canceled and refunded'),
)
ORDER_STATUS_CHOICES = (
    ('paid', 'Paid'),
    ('canceled_not_refunded', 'Canceled but not refunded'),
    ('canceled_refunded', 'Canceled and refunded'),
)


class AbstractOrder(models.Model):
    order_id = models.CharField(max_length=12, blank=True, help_text="Leave this field blank.")
    total = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Order: {} | pk: {} ".format(str(self.order_id), str(self.pk))

    def update_total(self):
        self.total = self.cart.total
        self.save()
        return self.total

    class Meta:
        abstract = True


class Order(AbstractOrder):
    cart = models.OneToOneField(Cart, null=True, on_delete=models.CASCADE, related_name="cart_order")
    status = models.CharField(max_length=256, default='created', choices=ORDER_STATUS_CHOICES)


class SoldOrder(AbstractOrder):
    cart = models.OneToOneField(SoldCart, null=True, on_delete=models.SET_NULL, related_name="cart_order")
    status = models.CharField(max_length=256, default='paid', choices=SOLD_ORDER_STATUS_CHOICES)

    def __str__(self):
        return "Order: {} | pk: {} ".format(str(self.order_id), str(self.pk))


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        qs = Order.objects.filter(cart=cart_obj)
        for obj in qs:
            obj.update_total()


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


pre_save.connect(pre_save_create_order_id, sender=Order)
post_save.connect(post_save_order, sender=Order)
post_save.connect(post_save_cart_total, sender=Cart)
