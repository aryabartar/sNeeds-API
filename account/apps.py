from django.apps import AppConfig
from django.db.backends.signals import connection_created


class AccountConfig(AppConfig):
    name = 'account'

