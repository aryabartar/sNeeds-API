import datetime

from django.core.management.base import BaseCommand

from sNeeds.apps.store.models import TimeSlotSale

DAYS = 1


# TODO: A user may be in process of buying time slot and this time deletes. Fix this later
class Command(BaseCommand):
    help = 'Closes TimeSlotSale instances with less than {} days to start'.format(DAYS)

    def handle(self, *args, **options):
        now = datetime.datetime.now()
        TimeSlotSale.objects.filter(start_time__lte=now + datetime.timedelta(days=DAYS)).delete()
