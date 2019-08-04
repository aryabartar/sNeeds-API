from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from sNeeds.apps.store.models import TimeSlotSale, SoldTimeSlotSale
from sNeeds.apps.discounts.models import TimeSlotSaleNumberDiscount

User = get_user_model()


class CartManager(models.QuerySet):
    def remove_time_slot_sale(self, time_slot):
        qs = self._chain()
        for obj in qs:
            obj.time_slot_sales.remove(time_slot)
        return qs

    @transaction.atomic
    def new_cart_with_time_sales(self, time_sales, **kwargs):
        obj = self.create(**kwargs)
        obj.time_slot_sales.add(*time_sales)
        return obj

    @transaction.atomic
    def set_cart_paid(self, cart):
        sold_cart_obj = SoldCart.objects.create(
            user=cart.user,
            subtotal=cart.subtotal,
            total=cart.total,
        )
        print("v")

        qs = cart.time_slot_sales.all().set_time_slot_sold(sold_to=cart.user)
        print("aa")
        sold_cart_obj.sold_time_slot_sales.add(*qs)
        sold_cart_obj.save()

        cart.delete()

        return sold_cart_obj


class AbstractCart(models.Model):
    subtotal = models.IntegerField(default=0.00, blank=True)
    total = models.IntegerField(default=0, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = CartManager.as_manager()

    class Meta:
        abstract = True


class Cart(AbstractCart):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time_slot_sales = models.ManyToManyField(TimeSlotSale, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def time_slot_sales_count(self):
        count = len(self.time_slot_sales.all())
        return count

    def __str__(self):
        return "User {} cart | pk: {}".format(self.user, str(self.pk))

    @transaction.atomic
    def set_time_slot_sales(self, time_slot_sales):
        for ts in time_slot_sales:
            self.time_slot_sales.add(ts)
        self.save()


class SoldCart(AbstractCart):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    sold_time_slot_sales = models.ManyToManyField(SoldTimeSlotSale, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "User {} cart | pk: {}".format(self.user, str(self.pk))

