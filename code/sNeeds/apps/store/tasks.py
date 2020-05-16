from celery import shared_task, task

from django.utils import timezone

from sNeeds.utils import sendemail
from .models import TimeSlotSale, SoldTimeSlotSale
from ...settings.config.variables import TIME_SLOT_SALE_DELETE_TIME, FRONTEND_URL
from ...utils.custom.time_functions import utc_to_jalali_string
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
def notify_sold_time_slot(send_to, name, sold_time_slot_url, start_time, end_time):
    sendemail.send_sold_time_slot_email(
        send_to, name, sold_time_slot_url, start_time, end_time
    )


@shared_task
def sold_time_slot_start_reminder():
    sts_qs = SoldTimeSlotSale.objects.filter(
        start_time__lte=timezone.now() + timezone.timedelta(days=1),
        start_time__gte=timezone.now(),
    )
    for obj in sts_qs:
        start_time = utc_to_jalali_string(obj.start_time)
        end_time = utc_to_jalali_string(obj.end_time)

        sold_time_slot_url = FRONTEND_URL + 'user/sessions/'

        send_sold_time_slot_start_reminder_email(
            sold_time_slot_url=sold_time_slot_url,
            send_to=obj.sold_to.email,
            name=obj.sold_to.get_full_name(),
            start_time=start_time,
            end_time=end_time
        )

        send_sold_time_slot_start_reminder_email(
            sold_time_slot_url=sold_time_slot_url,
            send_to=obj.consultant.user.email,
            name=obj.consultant.user.get_full_name(),
            start_time=start_time,
            end_time=end_time
        )
