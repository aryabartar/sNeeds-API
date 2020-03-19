from django.db import models, transaction
from sNeeds.apps.store.models import Product, SoldProduct, ProductQuerySet, SoldProductQuerySet


class WebinarManager(models.QuerySet):
    @transaction.atomic
    def add_webinar_sold(self, sold_to):
        qs = self.all()

        sold_webinars_list = []
        for obj in qs:
            sold_webinars_list.append(
                SoldWebinar.objects.create(
                    webinar=obj,
                    sold_to=sold_to,
                    price=obj.price,
                )
            )
        sold_webinars_qs = SoldWebinar.objects.filter(id__in=[obj.id for obj in sold_webinars_list])

        return sold_webinars_qs


class Webinar(Product):
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    active = models.BooleanField(default=True)
    objects = WebinarManager.as_manager()

    def __str__(self):
        return self.slug


class SoldWebinar(SoldProduct):
    webinar = models.ForeignKey(Webinar, on_delete=models.PROTECT)

    objects = SoldProductQuerySet.as_manager()

