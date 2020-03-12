from celery import shared_task, task

from django.utils import timezone

from sNeeds.utils import sendemail

from .models import TimeSlotSale, SoldTimeSlotSale
from ...settings.config.variables import TIME_SLOT_SALE_DELETE_TIME
from ...utils.sendemail import send_sold_time_slot_start_reminder_email


@shared_task
def delete_time_slots():
    """
    Deletes time slots with less than _ hours to start.
    """
    qs = TimeSlotSale.objects.filter(
        start_time__lte=timezone.now() + timezone.timedelta(hours=TIME_SLOT_SALE_DELETE_TIME)
    )
    qs.delete()


@shared_task
def send_notify_sold_time_slot_mail(send_to, name, sold_time_slot_id):
    sendemail.notify_sold_time_slot(
        send_to,
        name,
        sold_time_slot_id
    )


@shared_task
def sold_time_slot_start_reminder():
    sts_qs = SoldTimeSlotSale.objects.filter(start_time__lte=timezone.now() + timezone.timedelta(days=1), used=False)
    for obj in sts_qs:
        send_sold_time_slot_start_reminder_email(
            send_to=obj.sold_to.email,
            name=obj.sold_to.get_full_name(),
            sold_time_slot_id=obj.id,
            start_time=obj.start_time,
            end_time=obj.end_time
        )
        send_sold_time_slot_start_reminder_email(
            send_to=obj.consultant.email,
            name=obj.consultant.get_full_name(),
            sold_time_slot_id=obj.id,
            start_time=obj.start_time,
            end_time=obj.end_time
        )
