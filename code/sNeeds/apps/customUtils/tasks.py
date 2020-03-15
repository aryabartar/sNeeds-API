from django.core.management import call_command

from celery import task, shared_task


@shared_task
def backup_database():
    call_command('dbbackup')

