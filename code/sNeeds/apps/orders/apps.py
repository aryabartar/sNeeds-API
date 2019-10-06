from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'sNeeds.apps.orders'

    def ready(self):
        import sNeeds.apps.orders.signals.handlers
