from django.db import models

from sNeeds.apps.carts.models import Cart

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):
    order_id = models.CharField(max_length=12)
    cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=256, default='created', choices=ORDER_STATUS_CHOICES)
    total = models.DecimalField(max_digits=100, decimal_places=2)
