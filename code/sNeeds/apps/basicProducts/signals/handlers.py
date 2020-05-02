from django.db.models.signals import post_save, pre_save, post_init

from ..models import ClassWebinar, ClassWebinarPrice


def pre_save_update_price_class_webinar_object(sender, instance, *args, **kwargs):
    if instance.early:
        instance.price = instance.specialized_price.early_price
    else:
        instance.price = instance.specialized_price.regular_price


def pre_save_update_class_webinar_price_object_specialized_prices(sender, instance, *args, **kwargs):
    qs = ClassWebinar.objects.filter(specialized_price_id=instance.id)
    for obj in qs:
        if obj.early:
            obj.price = instance.early_price
        else:
            obj.price = instance.regular_price


pre_save.connect(pre_save_update_price_class_webinar_object, sender=ClassWebinar)
pre_save.connect(pre_save_update_class_webinar_price_object_specialized_prices, sender=ClassWebinarPrice)
