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
            new_sold_store_package = SoldStorePackage.objects.create(
                title=obj.title,
                price=obj.price,
                sold_to=sold_to,
            )
            sold_store_package_list.append(new_sold_store_package)

            store_package_phase_through_qs = StorePackagePhaseThrough.objects.filter(
                store_package=obj
            )

            for store_package_phase_through_obj in store_package_phase_through_qs:

                paid = False
                if store_package_phase_through_obj.phase_number == 1:
                    paid = True

                new_sold_store_package.sold_store_package_phases.create(
                    title=store_package_phase_through_obj.store_package_phase.title,
                    detailed_title=store_package_phase_through_obj.store_package_phase.detailed_title,
                    price=store_package_phase_through_obj.store_package_phase.price,
                    phase_number=store_package_phase_through_obj.phase_number,
                    paid=paid
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


class SoldStorePackagePhaseQuerySet(models.QuerySet):
    def get_qs_price(self):
        total = 0
        for obj in self._chain():
            total += obj.price
        return total


class SoldStorePackageQuerySet(models.QuerySet):
    def update_qs_prices(self):
        for obj in self._chain():
            obj.update_price()


class SoldStorePackage(SoldProduct):
    title = models.CharField(max_length=1024)
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.SET_NULL, blank=True, null=True)

    total_price = models.PositiveIntegerField()

    objects = SoldStorePackageQuerySet.as_manager()

    def _update_price(self):
        self.total_price = self.sold_store_package_phases.filter(paid=True).get_qs_price()

    def _update_total_price(self):
        self.price = self.sold_store_package_phases.all().get_qs_price()

    def update_price(self):
        self._update_price()
        self._update_total_price()
        self.save()

    # def __str__(self):
    #     return self.title


SOLD_STORE_PACKAGE_PHASE_STATUS = [
    ('not_started', "شروع نشده"),
    ("pay_to_start", "نیازمند پرداخت برای شروع"),
    ('in_progress', "در حال انجام"),
    ('done', "انجام شده")
]


class SoldStorePackagePhase(models.Model):
    title = models.CharField(max_length=1024)
    detailed_title = models.CharField(
        max_length=1024,
        help_text="This field is for ourselves, Feel free to add details."
    )
    sold_store_package = models.ForeignKey(
        SoldStorePackage,
        on_delete=models.CASCADE,
        related_name='sold_store_package_phases'
    )
    price = models.IntegerField(
        validators=[MinValueValidator(0), ],
    )
    phase_number = models.IntegerField()

    consultant_done = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    status = models.CharField(
        choices=SOLD_STORE_PACKAGE_PHASE_STATUS,
        default="not_started",
        max_length=128
    )

    objects = SoldStorePackagePhaseQuerySet.as_manager()

    class Meta:
        ordering = ['phase_number', ]

    # def update_status(self):
