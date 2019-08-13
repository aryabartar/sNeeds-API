from django.db.models.signals import post_save, pre_delete, pre_save, m2m_changed

from sNeeds.apps.videochats.models import Room


def pre_save_room_receiver(sender, instance, created, *args, **kwargs):
    if not instance.consultant_login_url:
        pass
    if not instance.consultant_login_url:
        pass


pre_save.connect(pre_save_room_receiver, sender=Room)
