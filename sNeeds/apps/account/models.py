from django.db import models
from django.contrib.auth.models import User


class Country (models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class University (models.Model):
    name = models.CharField(max_length=256, unique=True)
    country = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class FieldOfStudy (models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ConsultantProfile (models.Model):
    consultant = models.OneToOneField(
        User, on_delete=models.SET_NULL,  null=True)
    university = models.ManyToManyField(University)
    field_of_study = models.ManyToManyField(FieldOfStudy)
    country = models.ManyToManyField(Country)

    def __str__(self):
        return self.consultant.__str__()
