from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="user_information")
    phone = models.CharField(max_length=11)

    def __str__(self):
        return "{} information".format(self.user)
