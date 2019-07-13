from django.db import models

from sNeeds.apps.account.models import ConsultantProfile


class TimeSlotSale(models.Model):
    consultant = models.ForeignKey(ConsultantProfile,
                                   on_delete=models.CASCADE,
                                   related_name="time_slot_sales")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.IntegerField()

    def get_consultant_username(self):
        return self.consultant.user.username
