from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.contrib.auth import get_user_model

from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.store.models import Product, SoldProduct

User = get_user_model()


class StorePackageQuerySetManager(models.QuerySet):
    def update(self, **kwargs):
        super().update(**kwargs)
        for obj in self._chain():
            obj.save()

    @transaction.atomic
    def sell_and_get_sold_package(self, sold_to):
        qs = self.all()

        sold_store_package_list = []
        for obj in qs:
            sold_store_package_list.append(
                SoldStorePackage.objects.create(
                    store_package=obj,
                    price=obj.price,
                    sold_to=sold_to,
                )
            )
        sold_store_package_qs = SoldStorePackage.objects.filter(id__in=[obj.id for obj in sold_store_package_list])

        return sold_store_package_qs


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
        through='StorePackagePhaseThrough',
        related_name='store_packages'
    )
    total_price = models.PositiveIntegerField(blank=True)
    slug = models.SlugField(unique=True)

    objects = StorePackageQuerySetManager.as_manager()

    def _update_price(self):
        try:
            store_package_phase_through_obj = StorePackagePhaseThrough.objects.get(
                store_package__id=self.id, phase_number=1
            )
            self.price = store_package_phase_through_obj.store_package_phase.price
        except StorePackagePhaseThrough.DoesNotExist:
            self.price = 0

    def _update_total_price(self):
        store_package_phase_through_qs = StorePackagePhaseThrough.objects.filter(
            store_package__id=self.id,
        )
        total_price = 0
        for obj in store_package_phase_through_qs:
            total_price += obj.store_package_phase.price
        self.total_price = total_price

    def update_price(self):
        self._update_price()
        self._update_total_price()

    def clean(self):
        self.update_price()
        super().clean()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super(StorePackage, self).save()

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
    phase_number = models.IntegerField(
        validators=[MinValueValidator(0), ],
    )

    class Meta:
        unique_together = [
            ['store_package', 'phase_number'],
            ['store_package', 'store_package_phase']
        ]
        ordering = ['phase_number', ]


class SoldStorePackage(models.Model):
    store_package = models.ForeignKey(StorePackage, on_delete=models.SET_NULL, null=True)
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.SET_NULL, null=True)
    sold_to = models.ForeignKey(User, on_delete=models.PROTECT)


class SoldStorePackagePhase(SoldProduct):
    title = models.CharField(max_length=1024)
    detailed_title = models.CharField(
        max_length=1024,
        help_text="This field is for ourselves, Feel free to add details."
    )
    sold_store_package = models.ForeignKey(SoldStorePackage, on_delete=models.CASCADE)


class UnpaidStorePackagePhase(models.Model):
    title = models.CharField(max_length=1024)
    detailed_title = models.CharField(
        max_length=1024,
        help_text="This field is for ourselves, Feel free to add details."
    )
    price = models.IntegerField(
        validators=[MinValueValidator(0), ],
    )
    sold_store_package = models.ForeignKey(SoldStorePackage, on_delete=models.CASCADE)
