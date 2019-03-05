from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'


class TasksConfig(AppConfig):
    name = 'tasks'
    verbose_name = "Tasks"

    def ready(self):
        import account.signals.handlers
