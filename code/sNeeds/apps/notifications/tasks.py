from celery import shared_task, task

from django.utils import timezone
from sNeeds.apps.notifications.models import EmailNotification


@shared_task
def send_email_notifications():
    """
    Deletes time slots with less than _ hours to start.
    """
    qs = EmailNotification.objects.filter(
        send_date__lte=timezone.now(),
        sent=False
    )
    qs.update(sent=True)
