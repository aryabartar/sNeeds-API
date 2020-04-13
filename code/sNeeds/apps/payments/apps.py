from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    name = 'sNeeds.apps.payments'

    def ready(self):
        import sNeeds.apps.payments.signals.handlers
