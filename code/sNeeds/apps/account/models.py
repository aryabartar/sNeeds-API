import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from .validators import validate_resume_file_extension, validate_resume_file_size

from . import validators

User = get_user_model()

SEMESTER_CHOICES = [
    ('بهار', 'بهار'),
    ('تابستان', 'تابستان'),
    ('پاییز', 'پاییز‍'),
    ('زمستان', 'زمستان'),
]

"Attention"
"the names must be the same as the field names in the model."
STUDENT_FORM_CATEGORY_CHOICES = [
    ('grade', 'grade'),
    ('major', 'major'),
    ('university', 'university'),
    ('apply_grade', 'apply_grade'),
    ('apply_major', 'apply_major'),
    ('apply_country', 'apply_country'),
    ('apply_mainland', 'apply_mainland'),
    ('marital_status', 'marital_status'),
    ('apply_university', 'apply_university'),
    ('language_certificate', 'language_certificate'),
    ('degree_conferral_year', 'degree_conferral_year'),
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


class StudentFormFieldsChoice(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True, help_text="Lowercase pls")
    category = models.CharField(max_length=256, choices=STUDENT_FORM_CATEGORY_CHOICES)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class StudentFormApplySemesterYear(models.Model):
    year = models.PositiveSmallIntegerField()
    semester = models.CharField(max_length=64, choices=SEMESTER_CHOICES)

    class Meta:
        ordering = ["year", "semester"]

    def __str__(self):
        return str(self.year) + " " + self.semester


class StudentDetailedInfo(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Personal information
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(15), MaxValueValidator(100)])
    marital_status = models.ForeignKey(StudentFormFieldsChoice, on_delete=models.PROTECT, related_name='marital_status')

    # Last grade info
    grade = models.ForeignKey(StudentFormFieldsChoice, on_delete=models.PROTECT, related_name='grade')
    university = models.CharField(max_length=256)
    degree_conferral_year = models.PositiveSmallIntegerField()
    major = models.CharField(max_length=256)
    total_average = models.DecimalField(max_digits=4, decimal_places=2)
    thesis_title = models.CharField(max_length=512, blank=True, null=True)

    # Language skills and certificates
    language_certificate = models.ForeignKey(StudentFormFieldsChoice, on_delete=models.PROTECT,
                                             related_name='language_certificate')
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
    apply_mainland = models.ForeignKey(StudentFormFieldsChoice, on_delete=models.PROTECT, related_name='apply_mainland')
    apply_country = models.ForeignKey(StudentFormFieldsChoice, on_delete=models.PROTECT, related_name='apply_country')
    apply_grade = models.ForeignKey(StudentFormFieldsChoice, on_delete=models.PROTECT, related_name='apply_grade')
    apply_major = models.CharField(max_length=256)
    apply_university = models.CharField(max_length=256)
    apply_semester_year = models.ForeignKey(StudentFormApplySemesterYear, on_delete=models.PROTECT,
                                            related_name='apply_semester_year')

    # Extra info
    comment = models.TextField(max_length=1024, null=True, blank=True)
    resume = models.FileField(upload_to=get_student_resume_path, null=True, blank=True,
                              validators=[FileExtensionValidator(allowed_extensions=['pdf']), validate_resume_file_size])

    def is_complete(self):
        # TODO: Hossein, implement this
        # always is True, if form is created it means all the credentials are provided
        return True
