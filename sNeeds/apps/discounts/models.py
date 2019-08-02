from django.db import models


class TimeSlotSaleNumberDiscountModelManager(models.Manager):
    def get_discount_or_none(self, number):
        try:
            obj = TimeSlotSaleNumberDiscount.objects.filter(number=number)
            return obj.discount
        except:
            return None


class TimeSlotSaleNumberDiscount(models.Model):
    number = models.IntegerField(unique=True)
    discount = models.FloatField()

    objects = TimeSlotSaleNumberDiscountModelManager

    def __str__(self):
        return self.number
