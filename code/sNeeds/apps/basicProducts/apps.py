from django.apps import AppConfig


class BasicProductConfig(AppConfig):
    name = 'sNeeds.apps.basicProducts'

    def ready(self):
        import sNeeds.apps.basicProducts.signals.handlers
