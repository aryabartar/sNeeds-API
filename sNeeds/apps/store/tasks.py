from celery import shared_task

from sNeeds.utils import sendemail


@shared_task
def send_notify_sold_time_slot_mail(send_to, name, sold_time_slot_id):
    print("start")
    sendemail.notify_sold_time_slot(
        send_to,
        name,
        sold_time_slot_id
    )
    print("done!")
