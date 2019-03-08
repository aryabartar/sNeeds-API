from django.db import models
from django.contrib.auth import get_user_model

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
