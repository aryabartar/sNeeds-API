from django.apps import AppConfig


class VideoChatsConfig(AppConfig):
    name = 'sNeeds.apps.videochats'

    def ready(self):
        import sNeeds.apps.videochats.signals.handlers
