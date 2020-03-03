from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.consultants.models import ConsultantProfile


class TimeSlotSaleNumberDiscountModelManager(models.Manager):
    def get_discount_or_zero(self, num):
        try:
            obj = self.get(number=num)
            return obj.discount
        except TimeSlotSaleNumberDiscount.DoesNotExist:
            return 0


class TimeSlotSaleNumberDiscount(models.Model):
    number = models.PositiveIntegerField(primary_key=True)
    discount = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    objects = TimeSlotSaleNumberDiscountModelManager()

    def __str__(self):
        return str(self.number)


class CICharField(models.CharField):
    def get_prep_value(self, value):
        return str(value).lower()


class ConsultantDiscount(models.Model):
    consultants = models.ManyToManyField(ConsultantProfile)
    percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    code = CICharField(max_length=128, unique=True)

    def __str__(self):
        return "{}%".format(str(self.percent))


class CartConsultantDiscount(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, )
    consultant_discount = models.ForeignKey(
        ConsultantDiscount,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (("cart", "consultant_discount"),)

    def __str__(self):
        return "cart {} discount".format(str(self.consultant_discount))
