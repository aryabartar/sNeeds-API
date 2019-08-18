from __future__ import absolute_import, unicode_literals
from datetime import datetime

from celery import task
from celery.utils.log import get_task_logger

from sNeeds.apps.store.models import SoldTimeSlotSale

logger = get_task_logger(__name__)


@task()
def task_number_one():
    # now = datetime.now()
    # qs = SoldTimeSlotSale.objects.filter(start_time__lte)
    pass