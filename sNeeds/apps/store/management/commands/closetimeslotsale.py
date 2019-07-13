import datetime

from django.core.management.base import BaseCommand, CommandError

from sNeeds.apps.store.models import TimeSlotSale

DAYS = 1


class Command(BaseCommand):
    help = 'Closes TimeSlotSale instances with less than {} days to start'.format(DAYS)

    def handle(self, *args, **options):
        now = datetime.datetime.now()
        TimeSlotSale.objects.filter(start_time__lte=now + datetime.timedelta(days=DAYS)).delete()
