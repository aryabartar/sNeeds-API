from celery import shared_task

from sNeeds.utils import sendemail

@shared_task
def send_accept_order_mail(email, name, order_id):
    print("hey")
    sendemail.accept_order(email, name, order_id)
