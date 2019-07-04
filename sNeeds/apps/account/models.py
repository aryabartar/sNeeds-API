from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(help_text="Lowercase pls")

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=256, unique=True)
    country = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(help_text="Lowercase pls")

    def __str__(self):
        return self.name


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(help_text="Lowercase pls")

    def __str__(self):
        self.name = self.name
        return self.name


class ConsultantProfile(models.Model):
    consultant = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True)
    university = models.ManyToManyField(University)
    field_of_study = models.ManyToManyField(FieldOfStudy)
    country = models.ManyToManyField(Country)
    slug = models.SlugField(help_text="lowercase pls")
    # profile_picture = models.ImageField(upload_to="consultant_profile_photo")
    aparat_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.consultant.__str__()
