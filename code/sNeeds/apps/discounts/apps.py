from django.apps import AppConfig


class DiscountsConfig(AppConfig):
    name = 'sNeeds.apps.discounts'

    def ready(self):
        import sNeeds.apps.discounts.signals.handlers
