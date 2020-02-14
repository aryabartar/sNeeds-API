from enum import Enum
from enumfields import EnumIntegerField

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from sNeeds.apps.account.models import get_consultant_image_path, get_consultant_resume_path, University, FieldOfStudy, \
    Country


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


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    class UserTypeChoices(Enum):
        student = 1
        consultant = 2

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
        if self.user_type == self.UserTypeChoices.consultant:
            return True
        return False

    def is_student(self):
        if self.user_type == self.UserTypeChoices.student:
            return True
        return False

    def set_user_type_consultant(self):
        self.user_type = self.UserTypeChoices.consultant
        self.save()

    def set_user_type_student(self):
        self.user_type = self.UserTypeChoices.student
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


class ConsultantProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        null=True,
        on_delete=models.SET_NULL,
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

    time_slot_price = models.PositiveIntegerField()

    def __str__(self):
        return self.user.__str__()
