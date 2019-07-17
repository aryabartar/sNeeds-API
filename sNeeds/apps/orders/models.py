from django.db import models
from django.db.models.signals import pre_save, post_save

from .utils import unique_order_id_generator
from sNeeds.apps.carts.models import Cart

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):
    order_id = models.CharField(max_length=12, blank=True, help_text="Leave this field blank.")
    cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=256, default='created', choices=ORDER_STATUS_CHOICES)
    total = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.order_id)

    def update_total(self):
        self.total = self.cart.total
        self.save()
        return self.total


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        qs = Order.objects.filter(cart=cart_obj)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


pre_save.connect(pre_save_create_order_id, sender=Order)
post_save.connect(post_save_order, sender=Order)
post_save.connect(post_save_cart_total, sender=Cart)
