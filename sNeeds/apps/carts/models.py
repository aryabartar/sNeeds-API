from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save, m2m_changed

from sNeeds.apps.store.models import TimeSlotSale

User = get_user_model()


class CartModelManager(models.Manager):
    def get_new_and_deactive_others(self, user, *args, **kwargs):
        qs = Cart.objects.filter(user=user, active=True)
        for obj in qs:
            obj.update(active=False)
        new_cart = self.create(**kwargs)
        return new_cart


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    time_slot_sales = models.ManyToManyField(TimeSlotSale, blank=True)
    total = models.IntegerField(default=0, blank=True)
    subtotal = models.IntegerField(default=0.00, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "User {} cart".format(self.user)


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
