from django.db import models
from sNeeds.apps.account.models import ConsultantProfile


# Create your models here.
class TimeSlotSale(models.Model):
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE,
                                   related_name="time_slot_sales_as_consultant")
    buyer = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE,
                              related_name="time_slot_sales_as_buyer")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.IntegerField()
