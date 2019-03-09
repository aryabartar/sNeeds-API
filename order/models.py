from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save

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
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=128, default="created", choices=ORDER_STATUS_CHOICES)
    total = models.DecimalField(default=0, max_digits=20, decimal_places=0)

    def __str__(self):
        return self.order_id


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)
