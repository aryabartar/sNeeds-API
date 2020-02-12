from django.db import models

from sNeeds.apps.store.models import SoldTimeSlotSale
from sNeeds.apps.customAuth.models import ConsultantProfile


class Room(models.Model):
    sold_time_slot = models.OneToOneField(SoldTimeSlotSale, on_delete=models.CASCADE)

    room_id = models.IntegerField(null=True, blank=True)

    user_id = models.IntegerField(null=True, blank=True)
    consultant_id = models.IntegerField(null=True, blank=True)

    user_login_url = models.URLField(max_length=1024, blank=True)
    consultant_login_url = models.URLField(max_length=1024, blank=True)

    created = models.DateTimeField(auto_now_add=True)
