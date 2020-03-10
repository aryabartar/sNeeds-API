from django.db import models
from sNeeds.apps.store.models import Product, SoldProduct
from sNeeds.apps.consultants.models import ConsultantProfile


class Webinar(Product):
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    active = models.BooleanField(default=True)


class SoldWebinar(SoldProduct):
    webinar = models.ForeignKey(Webinar, on_delete=models.PROTECT)
