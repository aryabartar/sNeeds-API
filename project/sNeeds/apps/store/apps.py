from django.apps import AppConfig


class StoreConfig(AppConfig):
    name = 'sNeeds.apps.store'

    def ready(self):
        import sNeeds.apps.store.signals.handlers
