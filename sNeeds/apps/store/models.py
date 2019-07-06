from django.db import models
from django.contrib.auth.models import User

from sNeeds.apps.account.models import ConsultantProfile


class TimeSlotSale(models.Model):
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE,
                                   related_name="time_slot_sales_as_consultant")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name="time_slot_sales_as_buyer")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.IntegerField()

    def get_consultant_username(self):
        return self.consultant.user.username

    def get_buyer_username(self):
        return self.buyer.username
