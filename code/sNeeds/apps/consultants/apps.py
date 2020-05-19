from django.apps import AppConfig


class ConsultantsConfig(AppConfig):
    name = 'sNeeds.apps.consultants'

    def ready(self):
        import sNeeds.apps.consultants.signals.handlers
