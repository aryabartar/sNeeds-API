from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction

from sNeeds.apps.orders.models import Order

User = get_user_model()


class PayPayment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    authority = models.CharField(max_length=1024)

    def __str__(self):
        return str(self.order)
