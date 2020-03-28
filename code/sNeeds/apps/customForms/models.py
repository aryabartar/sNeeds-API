from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from sNeeds.apps.account.models import get_student_resume_path
import datetime


def year_choices():
    return [(r, r) for r in range(2000, datetime.date.today().year+4)]


def current_year():
    return datetime.date.today().year


User = get_user_model()


def get_bug_image_path(instance, filename):
    return "images/bugs/{}/image/{}".format(instance.email, filename)


class BugReport(models.Model):
    picture = models.ImageField(blank=True, upload_to=get_bug_image_path)
    comment = models.CharField(max_length=1024)
    email = models.EmailField(blank=True, max_length=128)

    def __str__(self):
        return self.comment[:40]


class PackageForm(models.Model):
    # Personal information
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)])
    marital_status = models.CharField()

    # Last grade info
    grade = models.CharField()
    university = models.CharField()
    total_average = models.DecimalField(max_digits=4, decimal_places=2)
    degree_conferral_year = models.IntegerField(_('year'), choices=year_choices, default=current_year)
    major = models.CharField()
    thesis_title = models.CharField(max_length=512, blank=True, null=True)
    language_certificate = models.CharField()
    language_speaking = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                         null=True, blank=True)
    language_listening = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                          null=True, blank=True)
    language_writing = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                        null=True, blank=True)
    language_reading = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                        null=True, blank=True)

    mainland = models.CharField(max_length=32)
    country = models.CharField(max_length=128)
    apply_grade = models.CharField()
    apply_major = models.CharField()

    comment = models.TextField(max_length=1024, null=True, blank=True)
    resume = models.FileField(upload_to=get_student_resume_path, null=True, blank=True)
