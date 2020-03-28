from django.db import models


def get_image_upload_path(sub_dir):
    return "account/images/" + sub_dir


def get_consultant_image_path(instance, filename):
    return "account/images/consultants/{}/image/{}".format(instance.user.email, filename)


def get_consultant_resume_path(instance, filename):
    return "account/files/consultants/{}/resume/{}".format(instance.user.email, filename)


def get_student_resume_path(instance, filename):
    return "account/files/students/{}/resume/{}".format(instance.user.email, filename)


class Country(models.Model):
    name = models.CharField(max_length=256, unique=True)
    picture = models.ImageField(upload_to=get_image_upload_path("country-pictures"))
    slug = models.SlugField(unique=True, help_text="Lowercase pls")

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=256, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
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


