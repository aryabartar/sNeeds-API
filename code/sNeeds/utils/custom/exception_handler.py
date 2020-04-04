from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    """
    https://gist.github.com/twidi/9d55486c36b6a51bdcb05ce3a763e79f
    This handler is used to change model validation error to serializer's validation error.
    """
    if isinstance(exc, DjangoValidationError):
        exc = DRFValidationError(detail=exc.message_dict)

    return drf_exception_handler(exc, context)
