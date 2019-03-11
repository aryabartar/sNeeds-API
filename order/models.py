from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save

from sneeds.utils import unique_order_id_generator
from cart.models import Cart

User = get_user_model()

ORDER_STATUS_CHOICES = (
    ("created", "Created"),
    ("paid", "Paid"),
    ("refunded", "Refunded"),
)


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=128, default="created", choices=ORDER_STATUS_CHOICES)
    total = models.DecimalField(default=0, max_digits=20, decimal_places=0)

    def update_total(self):
        cart_total = self.cart.total
        self.total = cart_total
        self.save()
        return self.total

    def check_done(self):
        self.update_total()
        if self.total < 0:
            return False

    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status

    def __str__(self):
        return self.order_id


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart_id=cart_id)
        if qs.exists():
            if qs.count() == 1:
                order_obj = qs.first()
                order_obj.update_total()


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


pre_save.connect(pre_save_create_order_id, sender=Order)
post_save.connect(post_save_cart_total, sender=Cart)
post_save.connect(post_save_order, Order)
