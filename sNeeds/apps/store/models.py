from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from sNeeds.apps.account.models import ConsultantProfile

User = get_user_model()


class AbstractTimeSlotSale(models.Model):
    consultant = models.ForeignKey(ConsultantProfile,
                                   on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.IntegerField()

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

    class Meta:
        abstract = True


class TimeSlotSale(AbstractTimeSlotSale):
    pass


class SoldTimeSlotSale(models.Model):
    sold_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
