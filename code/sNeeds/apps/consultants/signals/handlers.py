from django.db import transaction
from django.db.models.signals import post_save, pre_delete, pre_save, m2m_changed
from django.utils import timezone

from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.store.models import TimeSlotSale


def post_save_consultant(sender, instance, *args, **kwargs):
    time_slots_qs = TimeSlotSale.objects.filter(consultant=instance)
    time_slots_qs.update(price=instance.time_slot_price)


post_save.connect(post_save_consultant, sender=ConsultantProfile)
