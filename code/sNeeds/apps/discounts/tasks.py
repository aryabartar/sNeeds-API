from celery import task

from django.utils import timezone

from .models import ConsultantDiscount


@task()
def activate_consultant_discount():
	print("activating consultant discount")
	qs = ConsultantDiscount.objects.filter(start_time__lte=timezone.now())
	qs.update(active=True)


@task()
def deactivate_consultant_discount():
	print("deactivating consultant discount")
	qs = ConsultantDiscount.objects.filter(end_time__lte=timezone.now())
	qs.update(active=False)
