from django.db.models.signals import post_save, pre_save
from django.urls import reverse

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.payments.models import ConsultantDepositInfo
from sNeeds.apps.orders.tasks import notify_order_created
from sNeeds.apps.payments.utils import unique_consultant_deposit_info_id_generator
from sNeeds.settings.config.variables import BACKEND_URL, FRONTEND_URL


def pre_save_create_tracing_code(sender, instance, *args, **kwargs):
    if not instance.consultant_deposit_info_id:
        instance.tracing_code = unique_consultant_deposit_info_id_generator(instance)


pre_save.connect(pre_save_create_tracing_code, sender=ConsultantDepositInfo)