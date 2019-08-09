from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from sNeeds.apps.carts.models import Cart
from sNeeds.apps.account.models import ConsultantProfile


class CartConsultantDiscountManager(models.Manager):
    def create_with_consultant_discount(self, consultant_discount, **kwargs):
        obj = self.create(**kwargs)
        obj.consultant_discount.add(*consultant_discount)
        obj.save()
        return obj


class TimeSlotSaleNumberDiscountModelManager(models.Manager):
    def get_discount_or_zero(self, number):
        try:
            obj = TimeSlotSaleNumberDiscount.objects.get(number=number)
            return obj.discount
        except:
            return 0


class TimeSlotSaleNumberDiscount(models.Model):
    number = models.IntegerField(unique=True)
    discount = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    objects = TimeSlotSaleNumberDiscountModelManager()

    def __str__(self):
        return str(self.number)


class ConsultantDiscount(models.Model):
    consultant = models.ManyToManyField(ConsultantProfile)
    percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    start = models.DateTimeField()
    end = models.DateTimeField()

    def clean(self):
        if self.end < self.start:
            raise ValidationError("Start time is before end time.")

    def __str__(self):
        return "{}%".format(str(self.percent))


class CartConsultantDiscount(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    consultant_discount = models.ForeignKey(ConsultantDiscount, on_delete=models.CASCADE)

    objects = CartConsultantDiscountManager()

    def __str__(self):
        return "cart {} discount".format(str(self.consultant_discount))
