from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from sNeeds.apps.comments.models import SoldTimeSlotRate

User = get_user_model()


def post_save_sold_time_slot_sale_rate(sender, instance, created, *args, **kwargs):
    if created:
        pass

post_save.connect(post_save_sold_time_slot_sale_rate, sender=SoldTimeSlotRate)
