from django.apps import AppConfig


class CartsConfig(AppConfig):
    name = 'sNeeds.apps.carts'

    def ready(self):
        import sNeeds.apps.carts.signals.handlers
