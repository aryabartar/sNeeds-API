from django.apps import AppConfig


class CustomAuthConfig(AppConfig):
    name = 'sNeeds.apps.customAuth'
    verbose_name = 'Auth'

    def ready(self):
        import sNeeds.apps.customAuth.signals.handlers
