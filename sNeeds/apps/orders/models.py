from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save, post_save

from .utils import unique_order_id_generator

from sNeeds.apps.carts.models import Cart, SoldCart
from sNeeds.apps.billing.models import BillingProfile

User = get_user_model()

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('canceled_not_refunded', 'Canceled but not refunded'),
    ('canceled_refunded', 'Canceled and refunded'),
)


class AbstractOrder(models.Model):
    order_id = models.CharField(max_length=12, blank=True, help_text="Leave this field blank.")
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_order")
    status = models.CharField(max_length=256, default='created', choices=ORDER_STATUS_CHOICES)
    total = models.IntegerField(default=0, null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Order: {} | pk: {} ".format(str(self.order_id), str(self.pk))

    def update_total(self):
        self.total = self.cart.total
        self.save()
        return self.total

    def set_paid(self):
        if not self.active:
            raise ValidationError("Order is not active.")
        if not self.status == "created":
            raise ValidationError("Order status is not created.")

        self.active = False
        self.status = "paid"
        self.cart.set_paid()

    def _check_order_owners(self):
        if self.cart.user != self.billing_profile.user:
            raise ValidationError("Billing profile and user is not same.")

    def _check_both_active(self):
        if self.active and not self.cart.active:
            raise ValidationError("Cart should be active too.")

    def clean(self):
        self._check_order_owners()
        self._check_both_active()

    class Meta:
        abstract = True


class Order(AbstractOrder):
    pass


class SoldOrder(AbstractOrder):
    cart = models.ForeignKey(SoldCart, null=True, on_delete=models.SET_NULL, related_name="cart_order")

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
