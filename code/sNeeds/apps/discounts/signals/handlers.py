from django.db.models.signals import pre_save, post_delete, m2m_changed, post_save
from sNeeds.apps.discounts.utils import unique_discount_code_generator
from sNeeds.apps.discounts.models import (
    TimeSlotSaleNumberDiscount,
    CartDiscount,
    Discount
)
from sNeeds.apps.carts.models import Cart


def post_save_time_slot_sale_number_discount(sender, instance, *args, **kwargs):
    qs = Cart.objects.all()
    for obj in qs:
        obj.update_price()


def post_delete_time_slot_sale_number_discount(sender, instance, *args, **kwargs):
    qs = Cart.objects.all()
    for obj in qs:
        obj.update_price()


def post_save_cart_discount(sender, instance, *args, **kwargs):
    cart = instance.cart
    cart.update_price()


def post_delete_cart_discount(sender, instance, *args, **kwargs):
    cart = instance.cart
    cart.update_price()


def post_save_discount(sender, instance, *args, **kwargs):
    qs = CartDiscount.objects.filter(discount=instance)

    # TODO Is possible to update a discount that the discount use_limit reached to zero????
    if instance.use_limit is not None:
        if instance.use_limit == 0:
            qs.delete()
            return

    for obj in qs:
        cart = obj.cart
        cart.update_price()


def m2m_changed_discount(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        qs = CartDiscount.objects.filter(discount=instance)
        for obj in qs:
            cart = obj.cart
            cart.update_price()


def pre_save_create_discount_code(sender, instance, *args, **kwargs):
    if not instance.code:
        instance.code = unique_discount_code_generator(instance)


post_save.connect(post_save_time_slot_sale_number_discount, sender=TimeSlotSaleNumberDiscount)
post_delete.connect(post_save_time_slot_sale_number_discount, sender=TimeSlotSaleNumberDiscount)
post_save.connect(post_save_cart_discount, sender=CartDiscount)
post_delete.connect(post_delete_cart_discount, sender=CartDiscount)
post_save.connect(post_save_discount, sender=Discount)
m2m_changed.connect(m2m_changed_discount, sender=Discount.consultants.through)
pre_save.connect(pre_save_create_discount_code, sender=Discount)
