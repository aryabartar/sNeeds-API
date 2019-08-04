from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete

from sNeeds.apps.account.models import ConsultantProfile

User = get_user_model()


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
                )
            )


        qs.delete()

        return sold_tome_slot_sales_list


class AbstractTimeSlotSale(models.Model):
    consultant = models.ForeignKey(
        ConsultantProfile,
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.IntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.pk)

    def get_consultant_username(self):
        return self.consultant.user.username

    def clean(self, *args, **kwargs):
        if self.end_time <= self.start_time:
            raise ValidationError('Start time should be lass than end time', code='invalid')

        super(AbstractTimeSlotSale, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(AbstractTimeSlotSale, self).save(*args, **kwargs)


class TimeSlotSale(AbstractTimeSlotSale):
    objects = TimeSlotSaleManager.as_manager()


class SoldTimeSlotSale(AbstractTimeSlotSale):
    sold_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    used = models.BooleanField(default=False)
