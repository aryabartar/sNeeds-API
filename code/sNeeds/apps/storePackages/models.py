from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.contrib.auth import get_user_model

from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.store.models import Product

User = get_user_model()


class StorePackageDetailPhase(models.Model):
    title = models.CharField(max_length=1024)
    price = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )


class StorePackageDetail(models.Model):
    title = models.CharField(max_length=1024)
    store_package_phases = models.ManyToManyField(
        StorePackageDetailPhase,
        through='StorePackageDetailPhaseThrough'
    )


class StorePackageDetailPhaseThrough(models.Model):
    store_package_detail = models.ForeignKey(
        StorePackageDetail,
        on_delete=models.PROTECT
    )
    store_package_detail_phase = models.ForeignKey(
        StorePackageDetailPhase,
        on_delete=models.PROTECT
    )
    order = models.IntegerField()


class StorePackage(Product):
    store_package_detail = models.ForeignKey(StorePackageDetail, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    consultant = models.ForeignKey(ConsultantProfile, models.SET_NULL, null=True)
