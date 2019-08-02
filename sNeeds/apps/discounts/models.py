from django.db import models


# Create your models here.
class TimeSlotSaleNumberDiscount(models.Model):
    number = models.IntegerField()
    discount = models.FloatField()
