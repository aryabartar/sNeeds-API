from django.db.models.signals import post_save, pre_save

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.orders.models import Order
from sNeeds.apps.orders.tasks import send_accept_order_mail
from sNeeds.apps.orders.utils import unique_order_id_generator


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


def post_save_send_order_created(sender, instance, created, *args, **kwargs):
    # if created:
    print("heh")
    send_accept_order_mail(instance.user.email, instance.user.get_full_name(), instance.id)


pre_save.connect(pre_save_create_order_id, sender=Order)
post_save.connect(post_save_send_order_created, sender=Order)
