from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.contrib.auth import get_user_model

from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.store.models import Product, SoldProduct

User = get_user_model()


class StorePackagePhase(models.Model):
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


class StorePackage(Product):
    title = models.CharField(max_length=1024)
    store_package_phases = models.ManyToManyField(
        StorePackagePhase,
        through='StorePackagePhaseThrough'
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class StorePackagePhaseThrough(models.Model):
    store_package = models.ForeignKey(
        StorePackage,
        on_delete=models.PROTECT
    )
    store_package_phase = models.ForeignKey(
        StorePackagePhase,
        on_delete=models.PROTECT
    )
    order = models.IntegerField(
        validators=[MinValueValidator(0), ],
    )

    class Meta:
        unique_together = [
            ['store_package', 'order'],
            ['store_package', 'store_package_phase']
        ]
        ordering = ['order', ]


class SoldStorePackage(SoldProduct):
    store_package = models.ForeignKey(StorePackage, on_delete=models.PROTECT)
    consultant = models.ForeignKey(ConsultantProfile, models.SET_NULL, null=True)
