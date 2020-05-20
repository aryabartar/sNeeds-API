from django.core.exceptions import ValidationError
from . import models
from django.utils.translation import gettext_lazy as _


def validate_marital_status(value):
    marital_status_choices = []
    for choice in models.MARITAL_STATUS_CHOICES:
        marital_status_choices.append(choice[0])

    if value not in marital_status_choices:
        raise ValidationError(_("Entered marital status is not in allowed marital status or has misspelling"))
    else:
        return value


def validate_grade(value):
    grade_choices = []

    for choice in models.GRADE_CHOICES:
        grade_choices.append(choice[0])

    if value not in grade_choices:
        raise ValidationError(_("Entered grade is not in allowed grades or has misspelling"))
    else:
        return value


def validate_apply_grade(value):
    apply_grade_choices = []

    for choice in models.APPLY_GRADE_CHOICES:
        apply_grade_choices.append(choice[0])

    if value not in apply_grade_choices:
        raise ValidationError(_("Entered apply grade is not in allowed apply grades or has misspelling"))
    else:
        return value


def validate_language_certificate(value):
    language_certificate_choices = []
    for choice in models.LANGUAGE_CERTIFICATE_CHOICES:
        language_certificate_choices.append(choice[0])

    if value not in language_certificate_choices:
        raise ValidationError(_("Entered language certificate is not in allowed apply grades or has misspelling"))
    else:
        return value


def validate_mainland(value):
    mainland_choices = []
    for choice in models.MAINLAND_CHOICES:
        mainland_choices.append(choice[0])

    if value not in mainland_choices:
        raise ValidationError(_("Entered mainland is not in allowed mainlands or has misspelling"))
    else:
        return value


def validate_resume_file_extension(value):
    if value.file.content_type != 'application/pdf':
        raise ValidationError('Only pdf file can be uploaded')
    else:
        return value


def validate_resume_file_size(value):
    filesize = value.size

    if filesize > 5242880:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    else:
        return value
