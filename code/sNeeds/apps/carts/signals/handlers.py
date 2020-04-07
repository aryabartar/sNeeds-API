from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, pre_delete, m2m_changed

from sNeeds.apps.carts.models import Cart


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    # TODO: Remove it from all carts
    if action == 'pre_add':
        # Due to this problem products active status is validated in many to many signal
        # https://stackoverflow.com/questions/7986510/django-manytomany-model-validation
        product_qs = kwargs.get('model').objects.filter(
            id__in=list(kwargs.get('pk_set'))
        )
        if not product_qs.are_all_active():
            raise ValidationError({"products": "All products should be active."})

    if action == 'post_add' or action == 'post_remove' or action == 'post_clear' or action == 'post_':
        instance.update_price()
        instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)
