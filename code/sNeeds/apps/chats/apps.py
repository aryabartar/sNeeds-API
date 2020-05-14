from django.apps import AppConfig


class ChatsConfig(AppConfig):
    name = 'sNeeds.apps.chats'

    def ready(self):
        import sNeeds.apps.chats.signals.handlers
