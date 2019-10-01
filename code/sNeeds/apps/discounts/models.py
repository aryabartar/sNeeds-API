from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.account.models import ConsultantProfile


class TimeSlotSaleNumberDiscountModelManager(models.Manager):
    def get_discount_or_zero(self, number):
        try:
            obj = TimeSlotSaleNumberDiscount.objects.get(number=number)
            return obj.discount
        except:
            return 0


class TimeSlotSaleNumberDiscount(models.Model):
    number = models.PositiveIntegerField(unique=True)
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
    consultant = models.ManyToManyField(ConsultantProfile)
    percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    code = CICharField(max_length=128, unique=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return "{}%".format(str(self.percent))

    def clean(self, *args, **kwargs):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time should be after End time.")


def validate_consultant_discount(discount):
    if not ConsultantDiscount.objects.get(id=discount).active:
        raise ValidationError("Discount {} doesn't exist.".format(discount))


class CartConsultantDiscount(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, )
    consultant_discount = models.ForeignKey(ConsultantDiscount, on_delete=models.CASCADE,
                                            validators=[validate_consultant_discount])

    class Meta:
        unique_together = (("cart", "consultant_discount"),)

    def __str__(self):
        return "cart {} discount".format(str(self.consultant_discount))
