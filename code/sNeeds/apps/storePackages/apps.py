from django.apps import AppConfig


class StorePackagesConfig(AppConfig):
    name = 'sNeeds.apps.storePackages'

    def ready(self):
        import sNeeds.apps.storePackages.signals.handlers
