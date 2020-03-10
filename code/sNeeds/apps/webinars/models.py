from django.db import models
from sNeeds.apps.store.models import Product, SoldProduct
from sNeeds.apps.consultants.models import ConsultantProfile


class Webinar(models.Model):
    consultants = models.OneToOneRel(
        ConsultantProfile,
    )
    strat_date = models.DateField()
    end_date = models.DateField()


class WebinarTimeSlot(Product):
    consultant = models.ForeignKey(
        ConsultantProfile,
        on_delete=models.CASCADE
    )
    webinar = models.ForeignKey(
        Webinar,
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
