from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.contrib.auth import get_user_model

from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.store.models import Product

User = get_user_model()


class StorePackageDetailPhase(models.Model):
    title = models.CharField(max_length=1024)
    detailed_title = models.CharField(
        max_length=1024,
        help_text="This field is for ourselves, Feel free to add details."
    )
    price = models.IntegerField(
        validators=[MinValueValidator(0), ],
    )

    def __str__(self):
        return self.detailed_title


class StorePackageDetail(models.Model):
    title = models.CharField(max_length=1024)
    store_package_phases = models.ManyToManyField(
        StorePackageDetailPhase,
        through='StorePackageDetailPhaseThrough'
    )

    def __str__(self):
        return self.title


class StorePackageDetailPhaseThrough(models.Model):
    store_package_detail = models.ForeignKey(
        StorePackageDetail,
        on_delete=models.PROTECT
    )
    store_package_detail_phase = models.ForeignKey(
        StorePackageDetailPhase,
        on_delete=models.PROTECT
    )
    order = models.IntegerField(
        validators=[MinValueValidator(0), ],
    )

    class Meta:
        unique_together = [
            ['store_package_detail', 'order'],
            ['store_package_detail', 'store_package_detail_phase']
        ]
        ordering = ['order', ]


class StorePackage(Product):
    store_package_detail = models.ForeignKey(StorePackageDetail, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    consultant = models.ForeignKey(ConsultantProfile, models.SET_NULL, null=True)
    slug = models.SlugField(unique=True)