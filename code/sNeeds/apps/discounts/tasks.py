from celery import task

from django.utils import timezone
from django.db.models import Q

from .models import Discount


@task()
def activate_discount():
	now = timezone.now()
	qs = Discount.objects.filter(
		Q(start_time__lte=now) & Q(end_time__gt=now)
	)
	qs.update(active=True)


@task()
def deactivate_discount():
	qs = Discount.objects.filter(end_time__lte=timezone.now())
	qs.delete()
