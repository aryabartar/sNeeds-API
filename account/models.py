from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.IntegerField(max_length=500, blank=True)
