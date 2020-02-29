from django.apps import AppConfig


class CommentsConfig(AppConfig):
    name = 'sNeeds.apps.comments'
    verbose_name = 'Comment'

    def ready(self):
        import sNeeds.apps.comments.signals.handlers
