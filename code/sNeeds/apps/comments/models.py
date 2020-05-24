from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

from sNeeds.apps.basicProducts.models import ClassWebinar, SoldClassWebinar, BasicProduct, SoldBasicProduct
from sNeeds.apps.consultants.models import ConsultantProfile
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


class SoldClassWebinarRateManager(models.QuerySet):
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


# class SoldBasicProductRateField(models.Model):
#     rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True)
#     basic_product_rate_field = models.ForeignKey(BasicProductRateField, on_delete=models.PROTECT)


class BasicProductRate(models.Model):
    basic_product = models.OneToOneField(BasicProduct, on_delete=models.CASCADE)
    avg_rate = models.FloatField(default=0, null=True, blank=True)


class BasicProductRateField(models.Model):
    name = models.CharField(max_length=32, null=True)
    avg_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True)
    basic_product_rate = models.ForeignKey(BasicProductRate, on_delete=models.PROTECT)


class SoldBasicProductRate(models.Model):
    sold_basic_product = models.OneToOneField(SoldBasicProduct, on_delete=models.CASCADE)
    rates = models.ManyToManyField(BasicProductRateField, through='SoldBasicProductRateFieldThrough')

    object = SoldClassWebinarRateManager.as_manager()


class SoldBasicProductRateFieldThrough(models.Model):
    sold_basic_product_rate = models.ForeignKey(SoldBasicProductRate, on_delete=models.CASCADE)
    basic_product_rate_field = models.ForeignKey(BasicProductRateField, on_delete=models.CASCADE)
    rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
