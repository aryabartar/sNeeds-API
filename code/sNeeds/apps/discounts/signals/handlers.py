from django.db.models.signals import pre_save, post_delete, m2m_changed, post_save

from sNeeds.apps.discounts.models import (
    TimeSlotSaleNumberDiscount,
    CartConsultantDiscount,
    ConsultantDiscount
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


def post_save_cart_consultant_discount(sender, instance, *args, **kwargs):
    cart = instance.cart
    cart.update_price()


def post_delete_cart_consultant_discount(sender, instance, *args, **kwargs):
    cart = instance.cart
    cart.update_price()


def post_save_consultant_discount(sender, instance, *args, **kwargs):
    qs = CartConsultantDiscount.objects.filter(consultant_discount=instance)
    for obj in qs:
        cart = obj.cart
        cart.update_price()


def m2m_changed_consultant_discount(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        qs = CartConsultantDiscount.objects.filter(consultant_discount=instance)
        for obj in qs:
            cart = obj.cart
            cart.update_price()


post_save.connect(post_save_time_slot_sale_number_discount, sender=TimeSlotSaleNumberDiscount)
post_delete.connect(post_save_time_slot_sale_number_discount, sender=TimeSlotSaleNumberDiscount)
post_save.connect(post_save_cart_consultant_discount, sender=CartConsultantDiscount)
post_delete.connect(post_delete_cart_consultant_discount, sender=CartConsultantDiscount)
post_save.connect(post_save_consultant_discount, sender=ConsultantDiscount)
m2m_changed.connect(m2m_changed_consultant_discount, sender=ConsultantDiscount.consultant.through)
