import string
import time

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task


@shared_task
def create_random_user_accounts():
    time.sleep(5)
    print("eee\n\n\neee\n\n\neee")
    time.sleep(5)
    print("eee\n\n\neee\n\n\neee")
    time.sleep(5)
    print("eee\n\n\neee\n\n\neee")
    time.sleep(5)
    print("eee\n\n\neee\n\n\neee")
    return None
