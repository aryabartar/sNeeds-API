import json

from django.db import transaction
from django.db.models.signals import post_save, pre_delete, pre_save, m2m_changed
from django.utils import timezone

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.notifications.models import EmailNotification
from sNeeds.apps.store.models import TimeSlotSale, SoldTimeSlotSale, Product
from sNeeds.apps.store.tasks import notify_sold_time_slot
from sNeeds.apps.chats.models import Chat
from sNeeds.settings.config.variables import FRONTEND_URL
from sNeeds.utils.custom.time_functions import utc_to_jalali_string
from sNeeds.utils.sendemail import send_sold_time_slot_start_reminder_email


def pre_delete_product_receiver(sender, instance, *args, **kwargs):
    """
    When TimeSlotSale obj deletes, no signal will not trigger.
    This signal fix this problem.
    """
    Cart.objects.filter(products=instance).remove_product(instance)


def pre_save_time_slot_receiver(sender, instance, *args, **kwargs):
    consultant = instance.consultant
    if instance.price is None:
        instance.price = consultant.time_slot_price


@transaction.atomic
def post_save_time_slot_sold_receiver(sender, instance, created, *args, **kwargs):
    # This is sent for consultants
    if created:
        sold_time_slot_url = FRONTEND_URL + "user/sessions/"
        start_time = utc_to_jalali_string(instance.start_time)
        end_time = utc_to_jalali_string(instance.end_time)

        notify_sold_time_slot.delay(
            send_to=instance.consultant.user.email,
            name=instance.consultant.user.get_full_name(),
            sold_time_slot_url=sold_time_slot_url,
            start_time=start_time,
            end_time=end_time
        )

        data_dict = {
            "name": instance.sold_to.get_full_name(),
            "sold_time_slot_url": sold_time_slot_url,
            "start_time": start_time,
            "end_time": end_time
        }

        # For student
        EmailNotification.objects.create_sold_time_slot_reminder(
            send_date=instance.start_time - timezone.timedelta(days=2),
            data_json=json.dumps(data_dict),
            email=instance.sold_to.email
        )
        EmailNotification.objects.create_sold_time_slot_reminder(
            send_date=instance.start_time - timezone.timedelta(hours=2),
            data_json=json.dumps(data_dict),
            email=instance.sold_to.email
        )

        data_dict["name"] = instance.consultant.user.get_full_name()

        # For consultant
        EmailNotification.objects.create_sold_time_slot_reminder(
            send_date=instance.start_time - timezone.timedelta(days=2),
            data_json=json.dumps(data_dict),
            email=instance.consultant.user.email
        )
        EmailNotification.objects.create_sold_time_slot_reminder(
            send_date=instance.start_time - timezone.timedelta(hours=2),
            data_json=json.dumps(data_dict),
            email=instance.consultant.user.email
        )


def post_save_product_receiver(sender, instance, *args, **kwargs):
    cart_qs = Cart.objects.filter(products__in=[instance])

    # Used when time slot sold price is changed and its signal is triggered to
    # update this model or product set active to False
    for obj in cart_qs:
        obj.update_products()
        obj.update_price()


def create_chat(sender, instance, *args, **kwargs):
    user = instance.sold_to
    consultant = instance.consultant
    if not Chat.objects.filter(user=user, consultant=consultant).exists():
        Chat.objects.create(user=user, consultant=consultant)


pre_save.connect(pre_save_time_slot_receiver, sender=TimeSlotSale)

post_save.connect(post_save_product_receiver, sender=Product)
# Signal is not fired when subclasses were updated.
# https://stackoverflow.com/questions/14758250/django-post-save-signal-on-parent-class-with-multi-table-inheritance
for subclass in Product.__subclasses__():
    post_save.connect(post_save_product_receiver, subclass)

post_save.connect(post_save_time_slot_sold_receiver, sender=SoldTimeSlotSale)
post_save.connect(create_chat, sender=SoldTimeSlotSale)

pre_delete.connect(pre_delete_product_receiver, sender=Product)
