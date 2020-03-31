from django.db import models, transaction
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from sNeeds.apps.account.models import get_student_resume_path
from django.utils.translation import gettext_lazy as _
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


MARITAL_STATUS_CHOICES = [
    ('married', 'Married'),
    ('single', 'Single'),
]

GRADE_CHOICES = [
    ('college', 'College'),
    ('bachelor', 'Bachelor'),
    ('master', 'Master'),
    ('doctorate', 'Doctorate'),
    ('associate', 'Associate'),
]

LANGUAGE_CERTIFICATE_CHOICES = [
    ('IELTS_academic', 'IELTS Academic'),
    ('IELTS_general', 'IELTS General'),
    ('TOEFL', 'TOEFL'),
    ('duolingo', 'Duolingo'),
    ('IAESTE', 'IAESTE')
]

MAINLAND_CHOICES = [
    ('asia', 'Asia'),
    ('europe', 'Europe'),
    ('north_america', 'North America'),
    ('australia', 'Australia'),
]


class PackageFormManager(models.QuerySet):

    @transaction.atomic
    def new_cart_with_products(self, products, **kwargs):
        obj = self.create(**kwargs)
        obj.products.add(*products)
        return obj


class PackageForm(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    # Personal information
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(15), MaxValueValidator(100)])
    marital_status = models.CharField(max_length=32, choices=MARITAL_STATUS_CHOICES)

    # Last grade info
    grade = models.CharField(max_length=64, choices=GRADE_CHOICES)
    university = models.CharField(max_length=128)
    total_average = models.DecimalField(max_digits=4, decimal_places=2)
    degree_conferral_year = models.IntegerField(_('year'), choices=year_choices(), default=current_year)
    major = models.CharField(max_length=128)
    thesis_title = models.CharField(max_length=512, blank=True, null=True)
    language_certificate = models.CharField(max_length=64, choices=LANGUAGE_CERTIFICATE_CHOICES)
    language_certificate_score = models.PositiveSmallIntegerField(null=True, blank=True)
    language_speaking = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                         null=True, blank=True)
    language_listening = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                          null=True, blank=True)
    language_writing = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                        null=True, blank=True)
    language_reading = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                        null=True, blank=True)

    mainland = models.CharField(max_length=32, choices=MAINLAND_CHOICES)
    country = models.CharField(max_length=128)
    apply_grade = models.CharField(max_length=64, choices=GRADE_CHOICES)
    apply_major = models.CharField(max_length=128)

    comment = models.TextField(max_length=1024, null=True, blank=True)
    resume = models.FileField(upload_to=get_student_resume_path, null=True, blank=True)
