from django.db.models.signals import post_save, pre_save
from django.urls import reverse

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.orders.models import Order
from sNeeds.apps.orders.tasks import notify_order_created
from sNeeds.apps.orders.utils import unique_order_id_generator
from sNeeds.settings.config.variables import BACKEND_URL, FRONTEND_URL


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


def post_save_send_order_created(sender, instance, created, *args, **kwargs):
    order_url = FRONTEND_URL + "user/orders/" + str(instance.id)
    notify_order_created.delay(instance.user.email, instance.user.get_full_name(), order_url)


pre_save.connect(pre_save_create_order_id, sender=Order)
post_save.connect(post_save_send_order_created, sender=Order)
