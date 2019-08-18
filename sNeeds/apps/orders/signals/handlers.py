from django.db.models.signals import post_save, pre_save

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.orders.models import SoldOrder, Order
from sNeeds.apps.orders.utils import unique_order_id_generator

from sNeeds.apps.orders import tasks


def sold_order_post_save_receiver(sender, instance, *args, **kwargs):
    created = kwargs['created']
    if created:
        user = instance.cart.user
        tasks.send_accept_order_mail.delay(user.email, user.get_full_name(), instance.order_id)


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


def pre_save_create_sold_order_id(sender, instance, *args, **kwargs):
    """
    Used when this model is inserted manually.
    """
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        qs = Order.objects.filter(cart=cart_obj)
        for obj in qs:
            obj.update_total()


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


pre_save.connect(pre_save_create_order_id, sender=Order)
pre_save.connect(pre_save_create_sold_order_id, sender=SoldOrder)

post_save.connect(post_save_order, sender=Order)
post_save.connect(post_save_cart_total, sender=Cart)
post_save.connect(sold_order_post_save_receiver, sender=SoldOrder)
