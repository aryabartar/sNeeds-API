import datetime
from enum import Enum

from django.core.validators import MinValueValidator, MaxValueValidator
from enumfields import EnumIntegerField

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from sNeeds.apps.account.models import get_student_resume_path


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class UserTypeChoices(Enum):
    student = 1
    consultant = 2


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    email = models.EmailField(_('email address'), unique=True, max_length=256)
    phone_number = models.CharField(_('phone number'), unique=True, max_length=11, blank=True, null=True)
    first_name = models.CharField(_('first name'), null=True, max_length=30, blank=True)
    last_name = models.CharField(_('last name'), null=True, max_length=150, blank=True)

    user_type = EnumIntegerField(enum=UserTypeChoices, default=UserTypeChoices.student)  # default is student
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def is_consultant(self):
        if self.user_type == UserTypeChoices.consultant:
            return True
        return False

    def is_student(self):
        if self.user_type == UserTypeChoices.student:
            return True
        return False

    def set_user_type_consultant(self):
        self.user_type = UserTypeChoices.consultant
        self.save()

    def set_user_type_student(self):
        self.user_type = UserTypeChoices.student
        self.save()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def update_instance(self, instance, **kwargs):
        for (key, value) in kwargs.items():
            setattr(instance, key, value)
        instance.save()


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)


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
    ('post_doc', 'Post Doctoral'),
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


def year_choices():
    return [(r, r) for r in range(2000, datetime.date.today().year + 4)]


def current_year():
    return datetime.date.today().year


class StudentDetailedInfo(models.Model):
    from django.contrib.auth import get_user_model
    User = get_user_model()
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




