from django.contrib.auth import get_user_model
from django.db import models, connection
from django.conf import settings


def get_image_upload_path(sub_dir):
    return "images/account/" + sub_dir


def get_consultant_image_path(instance, filename):
    return "images/account/consultants/{}/image/{}".format(instance.user.email, filename)


def get_consultant_resume_path(instance, filename):
    return "files/account/consultants/{}/resume/{}".format(instance.user.email, filename)


class Country(models.Model):
    name = models.CharField(max_length=256, unique=True)
    picture = models.ImageField(upload_to=get_image_upload_path("country-pictures"))
    slug = models.SlugField(unique=True, help_text="Lowercase pls")

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=256, unique=True)
    country = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to=get_image_upload_path("university-pictures"))
    slug = models.SlugField(unique=True, help_text="Lowercase pls")

    def __str__(self):
        return self.name


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to=get_image_upload_path("field-of-study-pictures"))
    slug = models.SlugField(unique=True, help_text="Lowercase pls")

    def __str__(self):
        self.name = self.name
        return self.name


class ConsultantProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="consultant_profile"
    )
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to=get_consultant_image_path)
    aparat_link = models.URLField(null=True, blank=True)
    resume = models.FileField(upload_to=get_consultant_resume_path, null=True, blank=True)
    slug = models.SlugField(unique=True, help_text="lowercase pls")
    universities = models.ManyToManyField(University, blank=True)
    field_of_studies = models.ManyToManyField(FieldOfStudy, blank=True)
    countries = models.ManyToManyField(Country, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.__str__()
