from django.db import models
from django.contrib.auth import get_user_model

from sNeeds.apps.store.models import TimeSlotSale

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    time_slot_sales = models.ManyToManyField(TimeSlotSale)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "User {} cart".format(self.user)
