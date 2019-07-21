from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.core.exceptions import ValidationError

from sNeeds.apps.store.models import TimeSlotSale

User = get_user_model()


class CartManager(models.Manager):
    @transaction.atomic
    def new_cart_with_time_sales(self, time_sales, **kwargs):
        obj = self.create(**kwargs)
        obj.time_slot_sales.add(*time_sales)
        return obj


class AbstractCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time_slot_sales = models.ManyToManyField(TimeSlotSale, blank=True)
    total = models.IntegerField(default=0, blank=True)
    subtotal = models.IntegerField(default=0.00, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    class Meta:
        abstract = True

    def __str__(self):
        return "User {} cart | pk: {}".format(self.user, str(self.pk))

    @transaction.atomic
    def set_time_slot_sales(self, time_slot_sales):
        for ts in time_slot_sales:
            self.time_slot_sales.add(ts)
        self.save()


class Cart(AbstractCart):
    updated = models.DateTimeField(auto_now=True)


class SoldCart(AbstractCart):
    pass


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        time_slot_sales = instance.time_slot_sales.all()
        total = 0
        for t in time_slot_sales:
            total += t.price
        instance.subtotal = total
        instance.save()


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    instance.total = instance.subtotal


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.time_slot_sales.through)
pre_save.connect(pre_save_cart_receiver, sender=Cart)
