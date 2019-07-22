from django.db import models, connection
from django.conf import settings


class Country(models.Model):
    name = models.CharField(max_length=256, unique=True)
    picture = models.ImageField(upload_to="country_pictures")
    slug = models.SlugField(help_text="Lowercase pls")

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=256, unique=True)
    country = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to="university_pictures")
    slug = models.SlugField(help_text="Lowercase pls")

    def __str__(self):
        return self.name


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to="field_of_study_pictures")
    slug = models.SlugField(help_text="Lowercase pls")

    def __str__(self):
        self.name = self.name
        return self.name


class ConsultantProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="consultant_profile")
    profile_picture = models.ImageField(upload_to="consultant_profile_pictures")
    aparat_link = models.URLField(null=True, blank=True)
    slug = models.SlugField(help_text="lowercase pls")
    universities = models.ManyToManyField(University, blank=True)
    field_of_studies = models.ManyToManyField(FieldOfStudy, blank=True)
    countries = models.ManyToManyField(Country, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.__str__()
