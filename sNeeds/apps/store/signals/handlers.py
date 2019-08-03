from django.db.models.signals import post_save, pre_delete, m2m_changed

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.store.models import TimeSlotSale, SoldTimeSlotSale
from sNeeds.utils.sendemail import notify_sold_time_slot


def pre_delete_time_slot_sale_receiver(sender, instance, *args, **kwargs):
    """
    When TimeSlotSale obj deletes, no signal will not trigger.
    This signal fix this problem.
    """
    Cart.objects.filter(time_slot_sales=instance).remove_time_slot_sale(instance)


def post_save_time_sold_sold_receiver(sender, instance, created, *args, **kwargs):
    if created:
        notify_sold_time_slot(
            instance.consultant.user.email,
            instance.consultant.user.get_full_name(),
            instance.id
        )


pre_delete.connect(pre_delete_time_slot_sale_receiver, sender=TimeSlotSale)
post_save.connect(post_save_time_sold_sold_receiver, sender=SoldTimeSlotSale)
