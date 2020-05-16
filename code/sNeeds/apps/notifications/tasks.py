from celery import shared_task, task

from django.utils import timezone

from sNeeds.apps.notifications.models import EmailNotification
from sNeeds.utils.sendemail import send_sold_time_slot_start_reminder_email


@shared_task
def send_email_notifications():
    """
    Deletes time slots with less than _ hours to start.
    """
    qs = EmailNotification.objects.filter(
        send_date__lte=timezone.now(),
        sent=False
    )

    for obj in qs:
        if obj.is_sold_time_slot_reminder():
            send_sold_time_slot_start_reminder_email(**obj.data_dict)

    qs.update(sent=True)
