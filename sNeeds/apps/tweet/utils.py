import datetime
from django.conf import settings
from django.utils import timezone


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'expires': timezone.now() + settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA'] - datetime.timedelta(seconds=200)
    }
