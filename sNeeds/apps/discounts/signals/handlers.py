from django.db.models.signals import pre_save, pre_delete, m2m_changed, post_save

from sNeeds.apps.discounts.models import TimeSlotSaleNumberDiscount
from sNeeds.apps.carts.models import Cart


def post_save_time_slot_sale_number_discount(sender, instance, *args, **kwargs):
    qs = Cart.objects.all()
    for obj in qs:
        # For triggering Cart post_save to update total
        obj.save()


post_save.connect(post_save_time_slot_sale_number_discount, sender=TimeSlotSaleNumberDiscount)
