from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.orders.models import Order

User = get_user_model()


class PayPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    authority = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order)


class ConsultantDepositInfo(models.Model):
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.PROTECT)
    consultant_deposit_info_id = models.CharField(unique=True, max_length=12, blank=True,
                                                  help_text="Leave this field blank, this will populate automatically."
                                                  )
    amount = models.PositiveIntegerField()
    comment = models.TextField(max_length=512, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
