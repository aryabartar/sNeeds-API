from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from sNeeds.apps.account.models import ConsultantProfile

User = get_user_model()


class TimeSlotSale(models.Model):
    consultant = models.ForeignKey(ConsultantProfile,
                                   on_delete=models.CASCADE,
                                   related_name="time_slot_sales")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.IntegerField()

    def get_consultant_username(self):
        return self.consultant.user.username

    def clean(self, *args, **kwargs):
        if self.end_time <= self.start_time:
            raise ValidationError('Start time should be lass than end time', code='invalid')

        super(TimeSlotSale, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(TimeSlotSale, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)


class SoldTimeSlotSale(models.Model):
    consultant = models.ForeignKey(ConsultantProfile,
                                   null=True,
                                   on_delete=models.SET_NULL,
                                   related_name="sold_time_slot_sales")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.IntegerField()
    sold_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.pk)
