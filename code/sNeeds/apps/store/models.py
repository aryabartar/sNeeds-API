from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from sNeeds.apps.consultants.models import ConsultantProfile

User = get_user_model()


class ProductQuerySet(models.QuerySet):
    def get_time_slot_sales(self):
        result_qs = TimeSlotSale.objects.none()
        for i in self.all():
            try:
                time_slot_sale = i.timeslotsale
                result_qs |= TimeSlotSale.objects.filter(pk=time_slot_sale.id)
            except TimeSlotSale.DoesNotExist:
                pass
        return result_qs

    def get_basic_products(self):
        from sNeeds.apps.basicProducts.models import BasicProduct
        result_qs = BasicProduct.objects.none()
        for i in self.all():
            try:
                basic_product = i.basicproduct
                result_qs |= BasicProduct.objects.filter(pk=basic_product.id)
            except BasicProduct.DoesNotExist:
                pass
        return result_qs

    def get_store_packages(self):
        from sNeeds.apps.storePackages.models import StorePackage

        result_qs = StorePackage.objects.none()
        for i in self.all():
            try:
                store_package = i.storepackage
                result_qs |= StorePackage.objects.filter(pk=store_package.id)
            except StorePackage.DoesNotExist:
                pass

        return result_qs

    def are_all_active(self):
        for p in self._chain():
            if not p.active:
                return False
        return True


class SoldProductQuerySet(models.QuerySet):
    def get_sold_time_slot_sales(self):
        result_qs = SoldTimeSlotSale.objects.none()
        for i in self.all():
            try:
                sold_time_slot_sale = i.soldtimeslotsale
                result_qs |= SoldTimeSlotSale.objects.filter(pk=sold_time_slot_sale.id)
            except SoldTimeSlotSale.DoesNotExist:
                pass
        return result_qs

    def get_sold_basic_products(self):
        from sNeeds.apps.basicProducts.models import SoldBasicProduct

        result_qs = SoldBasicProduct.objects.none()
        for i in self.all():
            try:
                sold_basic_product = i.soldbasicproduct
                result_qs |= SoldBasicProduct.objects.filter(pk=sold_basic_product)
            except SoldBasicProduct.DoesNotExist:
                pass
        return result_qs

    def get_sold_store_paid_package_phases(self):
        from sNeeds.apps.storePackages.models import SoldStorePaidPackagePhase

        result_qs = SoldStorePaidPackagePhase.objects.none()
        for i in self.all():
            try:
                sold_store_paid_package_phase = i.soldstorepaidpackagephase
                result_qs |= SoldStorePaidPackagePhase.objects.filter(pk=sold_store_paid_package_phase)
            except SoldStorePaidPackagePhase.DoesNotExist:
                pass
        return result_qs


class TimeSlotSaleManager(models.QuerySet):
    @transaction.atomic
    def set_time_slot_sold(self, sold_to):
        qs = self.all()

        sold_time_slot_sales_list = []
        for obj in qs:
            sold_time_slot_sales_list.append(
                SoldTimeSlotSale.objects.create(
                    consultant=obj.consultant,
                    start_time=obj.start_time,
                    end_time=obj.end_time,
                    price=obj.price,
                    sold_to=sold_to,
                    used=False
                )
            )
        sold_time_slot_sales_qs = SoldTimeSlotSale.objects.filter(id__in=[obj.id for obj in sold_time_slot_sales_list])

        qs.delete()

        return sold_time_slot_sales_qs


class Product(models.Model):
    price = models.PositiveIntegerField(blank=True)
    active = models.BooleanField(default=True)

    objects = ProductQuerySet.as_manager()


class TimeSlotSale(Product):
    consultant = models.ForeignKey(
        ConsultantProfile,
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    objects = TimeSlotSaleManager.as_manager()

    def get_consultant_username(self):
        return self.consultant.user.username

    def save(self, *args, **kwargs):
        self.full_clean()
        super(TimeSlotSale, self).save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        start_time = self.start_time
        end_time = self.end_time
        consultant = self.consultant

        # Check 1
        if end_time <= start_time:
            raise ValidationError(_("End time should be after start time"), code='invalid')

        # Check 2
        consultant_time_slot_sales = TimeSlotSale.objects.filter(consultant=consultant)
        conflicting_time_slot_sales = (
                consultant_time_slot_sales.filter(start_time__lt=start_time).filter(end_time__gt=start_time) |
                consultant_time_slot_sales.filter(start_time__lt=end_time).filter(end_time__gt=end_time) |
                consultant_time_slot_sales.filter(start_time=start_time)  # For same start time
        ).exclude(id=self.id)

        if conflicting_time_slot_sales:
            sessions_str = ','.join(str(session.id) for session in conflicting_time_slot_sales)
            # raise ValidationError("bug!")

            raise ValidationError({
                "start_time": _(
                    "Selected time cannot be chosen because "
                    "the time you chose conflicts with your other time slot sales: " +
                    str(sessions_str)),
            })

        # Check 3
        consultant_sold_time_slot = SoldTimeSlotSale.objects.filter(consultant=consultant)
        conflicting_sold_sessions = (
                consultant_sold_time_slot.filter(start_time__lt=start_time).filter(end_time__gt=start_time) |
                consultant_sold_time_slot.filter(start_time__lt=end_time).filter(end_time__gt=end_time) |
                consultant_sold_time_slot.filter(start_time=start_time)  # For same start time
        )
        if conflicting_sold_sessions:
            sessions_str = ','.join(str(session.id) for session in conflicting_sold_sessions)
            raise ValidationError({
                "start_time": _("Selected time cannot be chosen because " +
                                "the time you chose conflicts with these times you have sold before :" +
                                str(sessions_str)),
            })


class SoldProduct(models.Model):
    price = models.PositiveIntegerField()
    sold_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = SoldProductQuerySet.as_manager()


# TODO: sold and unsold intersections
class SoldTimeSlotSale(SoldProduct):
    used = models.BooleanField(default=False)
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.PROTECT)
    start_time = models.DateTimeField(blank=False, null=False)
    end_time = models.DateTimeField(blank=False, null=False)

    objects = SoldProductQuerySet.as_manager()

    def clean(self, *args, **kwargs):
        if self.end_time <= self.start_time:
            raise ValidationError(_("End time should be after start time"), code='invalid')
