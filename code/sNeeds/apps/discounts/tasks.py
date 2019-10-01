from celery import task

from django.utils import timezone
from django.db.models import Q

from .models import ConsultantDiscount


@task()
def activate_consultant_discount():
	now = timezone.now()
	qs = ConsultantDiscount.objects.filter(
		Q(start_time__lte=now) & Q(end_time__gt=now)
	)
	qs.update(active=True)


@task()
def deactivate_consultant_discount():
	qs = ConsultantDiscount.objects.filter(end_time__lte=timezone.now())
	qs.delete()
