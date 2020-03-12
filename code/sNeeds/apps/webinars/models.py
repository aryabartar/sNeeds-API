from django.db import models
from sNeeds.apps.store.models import Product, SoldProduct, ProductQuerySet, SoldProductQuerySet


class Webinar(Product):
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    active = models.BooleanField(default=True)
    objects = ProductQuerySet.as_manager()


class SoldWebinar(SoldProduct):
    webinar = models.ForeignKey(Webinar, on_delete=models.PROTECT)

    objects = SoldProductQuerySet.as_manager()

