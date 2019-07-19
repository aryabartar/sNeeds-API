from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save, m2m_changed

from sNeeds.apps.store.models import TimeSlotSale

User = get_user_model()


class CartModelManager(models.Manager):
    def get_new_and_deactive_others(self, user, *args, **kwargs):
        time_slot_sales = kwargs.get('time_slot_sales', None)

        Cart.objects.filter(user=user, active=True).update(active=False)
        new_cart = self.create(user=user)
        new_cart.set_time_slot_sales(time_slot_sales)

        return new_cart


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    time_slot_sales = models.ManyToManyField(TimeSlotSale, blank=True)
    total = models.IntegerField(default=0, blank=True)
    subtotal = models.IntegerField(default=0.00, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartModelManager()

    def set_time_slot_sales(self, time_slot_sales):
        for time_slot_sale in time_slot_sales:
            self.time_slot_sales.add(time_slot_sale)
        self.save()

    def __str__(self):
        return "User {} cart | pk: {}".format(self.user, str(self.pk))


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
