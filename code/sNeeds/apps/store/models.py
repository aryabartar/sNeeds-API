from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.store.validators import validate_sold_product_class_type

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


class TimeSlotSaleManager(models.QuerySet):
    @transaction.atomic
    def set_time_slot_sold(self, sold_to):
        qs = self.all()

        sold_tome_slot_sales_list = []
        for obj in qs:
            sold_tome_slot_sales_list.append(
                SoldTimeSlotSale.objects.create(
                    consultant=obj.consultant,
                    start_time=obj.start_time,
                    end_time=obj.end_time,
                    price=obj.price,
                    sold_to=sold_to,
                    used=False
                )
            )
        sold_tome_slot_sales_qs = SoldTimeSlotSale.objects.filter(id__in=[obj.id for obj in sold_tome_slot_sales_list])

        qs.delete()

        return sold_tome_slot_sales_qs


class Product(models.Model):
    price = models.PositiveIntegerField(blank=True)

    objects = ProductQuerySet.as_manager()


class TimeSlotSale(Product):
    consultant = models.ForeignKey(
        ConsultantProfile,
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    objects = TimeSlotSaleManager.as_manager()

    def __str__(self):
        return str(self.pk)

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
    sold_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = SoldProductQuerySet.as_manager()


# TODO: sold and unsold intersections
class SoldTimeSlotSale(SoldProduct):
    used = models.BooleanField(default=False)
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.PROTECT)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    objects = SoldProductQuerySet.as_manager()

    def clean(self, *args, **kwargs):
        if self.end_time <= self.start_time:
            raise ValidationError(_("End time should be after start time"), code='invalid')


class ConsultantAcceptSoldProductRequest(models.Model):
    sold_product = models.ForeignKey(
        SoldProduct,
        validators=[validate_sold_product_class_type],
        on_delete=models.CASCADE
    )
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['sold_product', 'consultant']
