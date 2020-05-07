import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from . import validators

User = get_user_model()

MARITAL_STATUS_CHOICES = [
    ('married', 'Married'),
    ('single', 'Single'),
]
GRADE_CHOICES = [
    ('college', 'College'),
    ('associate', 'Associate'),
    ('bachelor', 'Bachelor'),
    ('master', 'Master'),
    ('doctoral', 'Doctoral'),
]
APPLY_GRADE_CHOICES = [
    ('college', 'College'),
    ('associate', 'Associate'),
    ('bachelor', 'Bachelor'),
    ('master', 'Master'),
    ('doctoral', 'Doctoral'),
    ('post_doctoral', 'Post Doctoral'),
]
LANGUAGE_CERTIFICATE_CHOICES = [
    ('ielts_academic', 'IELTS Academic'),
    ('ielts_general', 'IELTS General'),
    ('toefl', 'TOEFL'),
    ('duolingo', 'Duolingo'),
    ('iaeste', 'IAESTE'),
    ('gre', 'GRE'),
    ('gmat', 'GMAT'),
]
MAINLAND_CHOICES = [
    ('asia', 'Asia'),
    ('europe', 'Europe'),
    ('north_america', 'North America'),
    ('australia', 'Australia'),
]


def current_year():
    return datetime.date.today().year


def get_image_upload_path(sub_dir):
    return "account/images/" + sub_dir


def get_student_resume_path(instance, filename):
    return "account/files/students/{}/resume/{}".format(instance.user.email, filename)


class Country(models.Model):
    name = models.CharField(max_length=256, unique=True)
    picture = models.ImageField(upload_to=get_image_upload_path("country-pictures"))
    slug = models.SlugField(unique=True, help_text="Lowercase pls")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=256, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to=get_image_upload_path("university-pictures"))
    slug = models.SlugField(unique=True, help_text="Lowercase pls")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to=get_image_upload_path("field-of-study-pictures"))
    slug = models.SlugField(unique=True, help_text="Lowercase pls")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        self.name = self.name
        return self.name


class StudentDetailedInfo(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    # Personal information
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(15), MaxValueValidator(100)])
    marital_status = models.CharField(max_length=32, choices=MARITAL_STATUS_CHOICES,
                                      validators=[validators.validate_marital_status])

    # Last grade info
    grade = models.CharField(max_length=64, choices=GRADE_CHOICES, validators=[validators.validate_grade])
    university = models.CharField(max_length=128)
    total_average = models.DecimalField(max_digits=4, decimal_places=2)
    degree_conferral_year = models.PositiveSmallIntegerField()
    major = models.CharField(max_length=128)
    thesis_title = models.CharField(max_length=512, blank=True, null=True)

    # Language skills and certificates
    language_certificate = models.CharField(max_length=64, choices=LANGUAGE_CERTIFICATE_CHOICES,
                                            validators=[validators.validate_language_certificate])
    language_certificate_overall = models.PositiveSmallIntegerField(null=True, blank=True)
    language_speaking = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                         null=True, blank=True)
    language_listening = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                          null=True, blank=True)
    language_writing = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                        null=True, blank=True)
    language_reading = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    # Apply info
    mainland = models.CharField(max_length=32, choices=MAINLAND_CHOICES, validators=[validators.validate_mainland, ])
    country = models.CharField(max_length=128)
    apply_grade = models.CharField(max_length=64, choices=APPLY_GRADE_CHOICES,
                                   validators=[validators.validate_apply_grade])
    apply_major = models.CharField(max_length=128)

    # Extra info
    comment = models.TextField(max_length=1024, null=True, blank=True)
    resume = models.FileField(upload_to=get_student_resume_path, null=True, blank=True)

    def is_complete(self):
        # TODO: Hossein, implement this
        return True
