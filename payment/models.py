from django.db import models
from django.contrib.auth import get_user_model

from classes.models import PublicClass

User = get_user_model()


class CartManager(models.Manager):
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    public_classes = models.ManyToManyField(PublicClass, blank=True)
    total = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    updates = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager

    def __str__(self):
        return str(self.id)
