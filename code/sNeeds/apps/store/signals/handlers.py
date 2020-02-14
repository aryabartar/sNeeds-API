from django.db.models.signals import post_save, pre_delete, pre_save, m2m_changed

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.store.models import TimeSlotSale, SoldTimeSlotSale
from sNeeds.utils.sendemail import notify_sold_time_slot
from sNeeds.apps.store.tasks import send_notify_sold_time_slot_mail


def pre_delete_time_slot_sale_receiver(sender, instance, *args, **kwargs):
    """
    When TimeSlotSale obj deletes, no signal will not trigger.
    This signal fix this problem.
    """
    Cart.objects.filter(products=instance).remove_product(instance)


def post_save_time_slot_sold_receiver(sender, instance, created, *args, **kwargs):
    if created:
        send_notify_sold_time_slot_mail.delay(
            instance.consultant.user.email,
            instance.consultant.user.get_full_name(),
            instance.id
        )
        pass


def post_save_time_slot_receiver(sender, instance, *args, **kwargs):
    cart_qs = Cart.objects.filter(products=instance)

    # Used when time slot sold price is changed and its signal is triggered to update this model
    for obj in cart_qs:
        obj.update_price()


# pre_delete.connect(pre_delete_time_slot_sale_receiver, sender=TimeSlotSale)
#
# post_save.connect(post_save_time_slot_receiver, sender=TimeSlotSale)
# post_save.connect(post_save_time_slot_sold_receiver, sender=SoldTimeSlotSale)
