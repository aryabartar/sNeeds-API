from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save, post_save

from .utils import unique_order_id_generator

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.billing.models import BillingProfile

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('canceled_not_refunded', 'Canceled but not refunded'),
    ('canceled_refunded', 'Canceled and refunded'),
)


class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, on_delete=models.SET_NULL)
    order_id = models.CharField(max_length=12, blank=True, help_text="Leave this field blank.")
    cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL)
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

    def set_paid_order(self):
        self.status = "paid"


    def _check_order_owners(self):
        if self.cart.user != self.billing_profile.user:
            raise ValidationError("Billing profile and user is not same.")

    def clean(self):
        self._check_order_owners()


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

    if instance.active:
        Order.objects.filter(
            billing_profile__user=instance.billing_profile.user,
            active=True
        ).exclude(id=instance.id).update(active=False)


def pre_save_pay_order_id(sender, instance, *args, **kwargs):
    old = Order.objects.get(pk=instance.pk)
    user = instance.billing_profile.user
    # Just paid
    if instance.status == "paid" and old.status == "created":
        instance.active = False
        cart = instance.cart
        time_slot_sales_qs = cart.time_slot_sales.all()
        for time_slot_sale in time_slot_sales_qs:
            time_slot_sale.sell_to(user)


pre_save.connect(pre_save_create_order_id, sender=Order)
pre_save.connect(pre_save_pay_order_id, sender=Order)
post_save.connect(post_save_order, sender=Order)
post_save.connect(post_save_cart_total, sender=Cart)
