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

