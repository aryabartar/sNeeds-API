from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class PublicClass(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField(help_text="120000 stands for 120 hezar tooman.")
    slug = models.SlugField(unique=True , null=True)

    def __str__(self):
        return self.title


class SoldPublicClass(models.Model):
    public_class = models.ForeignKey(PublicClass, null=True, on_delete=models.SET_NULL,
                                     related_name="sold_classes")
    user = get_user_model()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{user} | {public_class}".format(user=self.user, public_class=self.public_class)
