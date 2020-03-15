from celery import task, shared_task

from django.core.management import call_command



@shared_task
def backup_database():
    call_command('dbbackup')

