from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'sNeeds.apps.customAuth'
    verbose_name = 'Auth'

    def ready(self):
        import sNeeds.apps.customAuth.signals  # noqa
