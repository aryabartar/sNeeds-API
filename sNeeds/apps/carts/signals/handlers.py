from django.db.models.signals import pre_save, pre_delete, m2m_changed

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.discounts.models import TimeSlotSaleNumberDiscount


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.update_price()

        # For time slot sale count discount in the cart
        time_slot_sale_count = instance.time_slot_sales_count()
        count_discount = TimeSlotSaleNumberDiscount.objects.get_discount_or_zero(time_slot_sale_count)
        instance.total = instance.subtotal * ((100.0 - count_discount) / 100)

        instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.time_slot_sales.through)
