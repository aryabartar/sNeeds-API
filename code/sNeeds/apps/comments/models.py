from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

from sNeeds.apps.customAuth.models import ConsultantProfile
from sNeeds.apps.store.models import SoldTimeSlotSale

User = get_user_model()


class SoldTimeSlotRateManager(models.QuerySet):
    def get_average_rate_or_none(self):
        if self.count() == 0:
            return None

        rate_sum = 0
        for obj in self.all():
            rate_sum += obj.rate

        return rate_sum / self.count()


class ConsultantComment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "User : {} | Consultant : {}".format(str(self.user), str(self.consultant))


class ConsultantAdminComment(models.Model):
    comment = models.OneToOneField(ConsultantComment, on_delete=models.CASCADE, related_name="admin_reply")
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Comment {} Reply".format(self.comment)


class SoldTimeSlotRate(models.Model):
    sold_time_slot = models.OneToOneField(SoldTimeSlotSale, on_delete=models.CASCADE)
    rate = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    objects = SoldTimeSlotRateManager.as_manager()
