from django.db.models.signals import pre_save, pre_delete, m2m_changed

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.store.models import TimeSlotSale
from sNeeds.apps.discounts.models import TimeSlotSaleNumberDiscount


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        time_slot_sales = instance.time_slot_sales.all()
        total = 0
        for t in time_slot_sales:
            total += t.price
        instance.subtotal = total
        instance.save()


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    # For time slot sale count discount in the cart
    time_slot_sale_count = instance.time_slot_sales_count()
    count_discount = TimeSlotSaleNumberDiscount.objects.get_discount_or_zero(time_slot_sale_count)
    instance.total = instance.subtotal * ((100.0 - count_discount) / 100)


def pre_delete_time_slot_sale_receiver(sender, instance, *args, **kwargs):
    """
    When TimeSlotSale obj deletes, no signal will not trigger.
    This signal fix this problem.
    """
    Cart.objects.filter(time_slot_sales=instance).remove_time_slot_sale(instance)


pre_delete.connect(pre_delete_time_slot_sale_receiver, sender=TimeSlotSale)
m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.time_slot_sales.through)
pre_save.connect(pre_save_cart_receiver, sender=Cart)
