from django.apps import AppConfig


class BasicproductConfig(AppConfig):
    name = 'sNeeds.apps.basicProducts'

    def ready(self):
        import sNeeds.apps.basicProducts.signals.handlers
