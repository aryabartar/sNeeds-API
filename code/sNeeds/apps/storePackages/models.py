import os

from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.contrib.auth import get_user_model

from sNeeds.apps.account.models import StudentDetailedInfo
from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.store.models import Product, SoldProduct

User = get_user_model()

SOLD_STORE_PACKAGE_PHASE_STATUS = [
    ('not_started', "شروع نشده"),
    ("pay_to_start", "نیازمند پرداخت برای شروع"),
    ('in_progress', "در حال انجام"),
    ('done', "انجام شده")
]
SOLD_STORE_PACKAGE_PHASE_DETAIL_STATUS = [
    ("in_progress", "در حال انجام"),
    ("done", "انجام شد"),
    ("finished", "دریافت نتیجه"),
    ("pending_user_data", "دریافت اطلاعات کاربر"),
]
CONTENT_TYPE_LIMIT_CHOICE = models.Q(app_label='storePackages', model='soldstorepaidpackagephase') | \
                            models.Q(app_label='storePackages', model='soldstoreunpaidpackagephase')


def get_sold_store_package_phase_detail_file_upload_path(instance, file_name):
    return "storePackage/files/sold-store-package-phase-detail/{}/{}".format(instance.id, file_name)


def get_store_package_image_upload_path(instance, file_name):
    return "storePackage/images/store-package-images/{}/{}".format(instance.id, file_name)


def get_sold_store_package_image_upload_path(instance, file_name):
    return "storePackage/images/sold-store-package-images/{}/{}".format(instance.id, file_name)


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
                paid_price=obj.price,
                sold_to=sold_to,
            )
            if obj.image:
                new_sold_store_package.image.save(obj.image_name, obj.image, True)

            sold_store_package_list.append(new_sold_store_package)

            store_package_phase_through_qs = StorePackagePhaseThrough.objects.filter(
                store_package=obj
            )

            for store_package_phase_through_obj in store_package_phase_through_qs:
                if store_package_phase_through_obj.phase_number == 1:
                    SoldStorePaidPackagePhase.objects.create(
                        title=store_package_phase_through_obj.store_package_phase.title,
                        description=store_package_phase_through_obj.store_package_phase.description,
                        detailed_title=store_package_phase_through_obj.store_package_phase.detailed_title,
                        price=store_package_phase_through_obj.store_package_phase.price,
                        phase_number=store_package_phase_through_obj.phase_number,
                        sold_store_package=new_sold_store_package
                    )
                else:
                    SoldStoreUnpaidPackagePhase.objects.create(
                        title=store_package_phase_through_obj.store_package_phase.title,
                        description=store_package_phase_through_obj.store_package_phase.description,
                        detailed_title=store_package_phase_through_obj.store_package_phase.detailed_title,
                        price=store_package_phase_through_obj.store_package_phase.price,
                        phase_number=store_package_phase_through_obj.phase_number,
                        sold_store_package=new_sold_store_package,
                        active=False
                    )

        sold_store_package_qs = SoldStorePackage.objects.filter(id__in=[obj.id for obj in sold_store_package_list])

        return sold_store_package_qs


class StorePackagePhase(models.Model):
    title = models.CharField(max_length=1024)
    detailed_title = models.CharField(
        max_length=1024,
        help_text="This field is for ourselves, Feel free to add details."
    )
    description = RichTextField(null=True, blank=True)

    price = models.IntegerField(
        validators=[MinValueValidator(0), ],
    )

    def __str__(self):
        return self.detailed_title


class StorePackage(Product):
    title = models.CharField(max_length=1024)
    image = models.ImageField(
        blank=True, null=True, upload_to=get_store_package_image_upload_path
    )
    slug = models.SlugField(unique=True)

    store_package_phases = models.ManyToManyField(
        StorePackagePhase,
        through='StorePackagePhaseThrough',
        related_name='store_packages'
    )

    total_price = models.PositiveIntegerField(blank=True)

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

    @property
    def image_name(self):
        if self.image is None:
            return None
        return os.path.basename(self.image.name)

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
            obj.save()

    def get_filled_student_detailed_infos(self):
        returned_qs = self.none()
        for obj in self._chain():
            if StudentDetailedInfo.objects.filter(user=obj.sold_to).exists():
                returned_qs |= self.filter(id=obj.id)
        return returned_qs


class SoldStorePackage(models.Model):
    title = models.CharField(max_length=1024)
    image = models.ImageField(
        blank=False, null=True, upload_to=get_sold_store_package_image_upload_path
    )

    sold_to = models.ForeignKey(User, on_delete=models.PROTECT)
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.SET_NULL, blank=True, null=True)

    paid_price = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = SoldStorePackageQuerySet.as_manager()

    def _update_paid_price(self):
        paid_price = SoldStorePaidPackagePhase.objects.filter(
            sold_store_package__id=self.id
        ).get_qs_price()
        self.paid_price = paid_price

    def _update_total_price(self):
        paid_price = SoldStorePaidPackagePhase.objects.filter(
            sold_store_package__id=self.id
        ).get_qs_price()
        unpaid_price = SoldStoreUnpaidPackagePhase.objects.filter(
            sold_store_package__id=self.id
        ).get_qs_price()
        self.total_price = paid_price + unpaid_price

    def update_price(self):
        self._update_paid_price()
        self._update_total_price()


class SoldStorePackagePhaseQuerySet(models.QuerySet):
    def get_qs_price(self):
        qs_price = 0
        for obj in self._chain():
            qs_price += obj.price
        return qs_price


class SoldStorePaidPackagePhaseQuerySet(SoldStorePackagePhaseQuerySet):
    pass


class SoldStoreUnpaidPackagePhaseQuerySet(SoldStorePackagePhaseQuerySet):
    def deactivate_all(self):
        for obj in self._chain():
            obj.active = False
            obj.save()

    @transaction.atomic
    def sell_and_get_paid_phases(self):
        sold_store_paid_package_phases_list = []

        for obj in self._chain():
            new_obj = SoldStorePaidPackagePhase.objects.create(
                title=obj.title,
                detailed_title=obj.detailed_title,
                price=obj.price,
                phase_number=obj.phase_number,
                sold_store_package=obj.sold_store_package,
            )
            sold_store_paid_package_phases_list.append(new_obj)
            obj.delete()

        sold_store_paid_package_phases_qs = SoldStorePaidPackagePhase.objects.filter(
            id__in=[obj.id for obj in sold_store_paid_package_phases_list]
        )

        return sold_store_paid_package_phases_qs


class SoldStorePackagePhaseDetail(models.Model):
    title = models.CharField(max_length=1024, null=False, blank=False)
    status = models.CharField(
        choices=SOLD_STORE_PACKAGE_PHASE_DETAIL_STATUS,
        max_length=1024
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=CONTENT_TYPE_LIMIT_CHOICE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    file = models.FileField(
        blank=True, null=True, upload_to=get_sold_store_package_phase_detail_file_upload_path
    )

    def clean(self):
        if self.content_object is None:
            raise ValidationError({"object_id": "Id is not valid."})

    def save(self, *args, **kwargs):
        self.clean()
        super(SoldStorePackagePhaseDetail, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created']


class SoldStorePackagePhase(models.Model):
    title = models.CharField(max_length=1024)
    detailed_title = models.CharField(
        max_length=1024,
        help_text="This field is for ourselves, Feel free to add details."
    )
    description = RichTextField(null=True, blank=True)
    sold_store_package = models.ForeignKey(
        SoldStorePackage,
        on_delete=models.CASCADE,
    )

    phase_number = models.IntegerField()

    status = models.CharField(
        choices=SOLD_STORE_PACKAGE_PHASE_STATUS,
        default="not_started",
        max_length=128
    )

    class Meta:
        abstract = True
        ordering = ['phase_number', ]


class SoldStorePaidPackagePhase(SoldStorePackagePhase, SoldProduct):
    consultant_done = models.BooleanField(default=False)
    phase_detail = GenericRelation(
        SoldStorePackagePhaseDetail,
        related_query_name="sold_store_paid_package_phase"
    )

    objects = SoldStorePaidPackagePhaseQuerySet.as_manager()

    def get_status(self):
        if not self.consultant_done:
            return "in_progress"
        else:
            return "done"


class SoldStoreUnpaidPackagePhase(SoldStorePackagePhase, Product):
    objects = SoldStoreUnpaidPackagePhaseQuerySet.as_manager()
    phase_detail = GenericRelation(
        SoldStorePackagePhaseDetail,
        related_query_name="sold_store_unpaid_package_phase"
    )

    def get_status(self):
        if not self.active:
            return "not_started"
        else:
            return "pay_to_start"


class ConsultantSoldStorePackageAcceptRequest(models.Model):
    sold_store_package = models.ForeignKey(
        SoldStorePackage,
        on_delete=models.CASCADE
    )
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['sold_store_package', 'consultant']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super(ConsultantSoldStorePackageAcceptRequest, self).save()

    def clean(self):
        if self.sold_store_package.consultant is not None:
            raise ValidationError(
                {"sold_store_package": "This sold store package consultant is not None."}
            )
