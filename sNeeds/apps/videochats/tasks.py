from __future__ import absolute_import, unicode_literals
from celery import task

@task()
def task_number_one():
    # Do something...