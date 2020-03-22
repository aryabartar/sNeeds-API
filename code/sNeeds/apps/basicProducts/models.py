from django.db import models, transaction
from sNeeds.apps.store.models import Product, SoldProduct, ProductQuerySet, SoldProductQuerySet


class BasicProductManager(models.QuerySet):
    @transaction.atomic
    def add_basic_product_sold(self, sold_to):
        qs = self.all()

        sold_basic_product_list = []
        for obj in qs:
            sold_basic_product_list.append(
                SoldBasicProduct.objects.create(
                    basic_product=obj,
                    sold_to=sold_to,
                    price=obj.price,
                )
            )
        sold_basic_product_qs = SoldBasicProduct.objects.filter(id__in=[obj.id for obj in sold_basic_product_list])

        return sold_basic_product_qs


class BasicProduct(Product):
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    objects = BasicProductManager.as_manager()

    def __str__(self):
        return self.slug


class SoldBasicProduct(SoldProduct):
    basic_product = models.ForeignKey(BasicProduct, on_delete=models.PROTECT)

    objects = SoldProductQuerySet.as_manager()

