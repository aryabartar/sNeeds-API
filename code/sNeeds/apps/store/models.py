from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
    price = models.PositiveIntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.pk)

    def get_consultant_username(self):
        return self.consultant.user.username

    def save(self, *args, **kwargs):
        self.full_clean()
        super(AbstractTimeSlotSale, self).save(*args, **kwargs)


class TimeSlotSale(AbstractTimeSlotSale):
    objects = TimeSlotSaleManager.as_manager()

    def clean(self, *args, **kwargs):
        start_time = self.start_time
        end_time = self.end_time
        consultant = self.consultant
        sold_time_slot_of_consultant = SoldTimeSlotSale.objects.filter(consultant=consultant)
        conflicting_sold_sessions = (
          sold_time_slot_of_consultant.filter(start_time__lt=start_time).filter(end_time__gt=start_time) |
          sold_time_slot_of_consultant.filter(start_time__lt=end_time).filter(end_time__gt=end_time)
        )
        if conflicting_sold_sessions:
            sessions_str = ','.join(str(session.id) for session in conflicting_sold_sessions)
            raise ValidationError({
                "detail": _("Selected time cannot be chosen because " +
                                    "the time you chose conflicts with these times you have sold before "+
                                    str(sessions_str)),
                "conflicting_time_slots": sessions_str
            })

        time_slot_sale_of_consultant = TimeSlotSale.objects.filter(consultant=consultant)
        conflicting_sessions = (
            time_slot_sale_of_consultant.filter(start_time__lt=start_time).filter(end_time__gt=start_time) |
            time_slot_sale_of_consultant.filter(start_time__lt=end_time).filter(end_time__gt=end_time)
        )
        if conflicting_sessions:
            sessions_str = ','.join(str(session.id) for session in conflicting_sessions)
            raise ValidationError({
                "detail":_(
                "Selected time cannot be chosen because "
                "the time you chose conflicts with other times you have chosen before " +
                sessions_str),
                "conflicting_time_slots": sessions_str
            })
        if end_time <= start_time:
            raise ValidationError(_("End Time should be after Start time"), code='invalid')


class SoldTimeSlotSale(AbstractTimeSlotSale):
    sold_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    used = models.BooleanField(default=False)
