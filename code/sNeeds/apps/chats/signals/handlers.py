from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model

from sNeeds.apps.chats.models import Chat

User = get_user_model()


def post_save_user(sender, instance, created, *args, **kwargs):
    if created:
        admin_consultant_user = User.objects.get_admin_consultant_or_none()
        if admin_consultant_user is not None:
            chat = Chat.objects.get_or_create(
                user=instance,
                consultant=admin_consultant_user
            )


post_save.connect(post_save_user, sender=User)
