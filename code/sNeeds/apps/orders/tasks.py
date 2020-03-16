from celery import shared_task

from sNeeds.utils import sendemail

@shared_task
def notify_order_created(email, name, order_url):
    sendemail.send_order_created_email(email, name, order_url)
