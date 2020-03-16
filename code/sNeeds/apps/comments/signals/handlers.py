from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model

from sNeeds.apps.comments.models import SoldTimeSlotRate

User = get_user_model()


def post_save_sold_time_slot_sale_rate(sender, instance, created, *args, **kwargs):
    instance.sold_time_slot.consultant.update_rate()


def post_delete_sold_time_slot_sale_rate(sender, instance, *args, **kwargs):
    instance.sold_time_slot.consultant.update_rate()


post_save.connect(post_save_sold_time_slot_sale_rate, sender=SoldTimeSlotRate)
post_delete.connect(post_delete_sold_time_slot_sale_rate, sender=SoldTimeSlotRate)
