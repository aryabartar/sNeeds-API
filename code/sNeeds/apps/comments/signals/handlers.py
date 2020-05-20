from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model

from sNeeds.apps.basicProducts.models import SoldBasicProduct
from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.comments.models import SoldTimeSlotRate, SoldBasicProductRateFieldThrough, BasicProductRateField

User = get_user_model()


def post_save_sold_time_slot_sale_rate(sender, instance, created, *args, **kwargs):
    instance.sold_time_slot.consultant.update_rate()


def post_delete_sold_time_slot_sale_rate(sender, instance, *args, **kwargs):
    instance.sold_time_slot.consultant.update_rate()


def post_save_sold_basic_product_rate_field_through(sender, instance, created, *args, **kwargs):
    rate_field = instance.basic_product_rate_field
    rate_field_rates_qs = SoldBasicProductRateFieldThrough.objects.filter(basic_product_rate_field=rate_field)

    rate_sum = 0
    for obj in rate_field_rates_qs:
        rate_sum += obj.rate

    rate_field.avg_rate = rate_sum / rate_field_rates_qs.count()
    rate_field.save()


def post_save_basic_product_rate_field(sender, instance, created, *args, **kwargs):
    rate_fields_qs = BasicProductRateField.objects.filter(basic_product_rate=instance.basic_product_rate)
    rate_sum = 0
    for obj in rate_fields_qs:
        rate_sum += obj.avg_rate

    instance.basic_product_rate.avg_rate = rate_sum / rate_fields_qs.count()
    instance.basic_product_rate.save()


post_save.connect(post_save_sold_time_slot_sale_rate, sender=SoldTimeSlotRate)
post_delete.connect(post_delete_sold_time_slot_sale_rate, sender=SoldTimeSlotRate)
post_save.connect(post_save_sold_basic_product_rate_field_through, sender=SoldBasicProductRateFieldThrough)
post_save.connect(post_save_basic_product_rate_field, sender=BasicProductRateField)
