from django.core.exceptions import ValidationError
from . import models
from django.utils.translation import gettext_lazy as _


def validate_marital_status(value):
    pass


def validate_grade(value):
    pass


def validate_apply_grade(value):
    pass


def validate_language_certificate(value):
    pass


def validate_mainland(value):
    pass


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
