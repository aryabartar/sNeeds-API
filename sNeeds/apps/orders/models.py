from django.db import models
from django.db.models.signals import pre_save

from .utils import unique_order_id_generator
from sNeeds.apps.carts.models import Cart

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):
    order_id = models.CharField(max_length=12, blank=True)
    cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=256, default='created', choices=ORDER_STATUS_CHOICES)
    total = models.DecimalField(max_digits=100, decimal_places=2)


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)
