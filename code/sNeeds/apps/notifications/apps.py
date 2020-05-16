from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'sNeeds.apps.notifications'
    verbose_name = 'Notification'

    def ready(self):
        import sNeeds.apps.notifications.signals.handlers
