from enum import Enum

from django.core.exceptions import ValidationError
from enumfields import EnumIntegerField

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


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
    admin_consultant = 3  # For automatic chat and ...


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

    user_type = EnumIntegerField(
        enum=UserTypeChoices,
        default=UserTypeChoices.student,
    )
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

        if self.user_type == UserTypeChoices.admin_consultant:
            if CustomUser.objects.filter(user_type=UserTypeChoices.admin_consultant).exclude(id=self.id).exists():
                raise ValidationError("User with admin_consultant type exists.")

        self.update_user_type()

        self.email = self.__class__.objects.normalize_email(self.email)
        self.email = self.email.lower()

    def update_user_type(self):
        from sNeeds.apps.consultants.models import ConsultantProfile
        if self.user_type == UserTypeChoices.admin_consultant:
            return

        if ConsultantProfile.objects.filter(user__id=self.id).exists():
            self.user_type = UserTypeChoices.consultant
        else:
            self.user_type = UserTypeChoices.student

    def is_consultant(self):
        if self.user_type == UserTypeChoices.consultant:
            return True
        return False

    def is_student(self):
        if self.user_type == UserTypeChoices.student:
            return True
        return False

    def is_admin_consultant(self):
        if self.user_type == UserTypeChoices.admin_consultant:
            return True
        return False

    def set_user_type_consultant(self):
        self.user_type = UserTypeChoices.consultant
        self.save()

    def set_user_type_student(self):
        self.user_type = UserTypeChoices.student
        self.save()

    def set_user_admin_consultant(self):
        self.user_type = UserTypeChoices.admin_consultant
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
