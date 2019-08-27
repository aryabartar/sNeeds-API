from django.db import models
from django.core import validators

from sNeeds.apps.account.models import ConsultantProfile


def path_for_uploading_file(instance, filename):
    return "media/tmp_consultant/{email}/{filename}".format(email=instance.email, filename=filename)


class TMPConsultant(models.Model):
    first_name = models.CharField(max_length=128, null=False, blank=False)
    last_name = models.CharField(max_length=128, null=False, blank=False)
    email = models.EmailField(max_length=64, null=False, blank=False,)
    phone_number = models.CharField(max_length=11, null=False, blank=False)
    university = models.CharField(max_length=256, blank=False, null=False)
    field_of_study = models.CharField(max_length=256, blank=False, null=False)
    resume = models.FileField(upload_to=path_for_uploading_file, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)