from django.db.models.signals import post_save, post_delete, pre_save, m2m_changed

from sNeeds.apps.videochats.models import Room
from sNeeds.apps.videochats.utils import create_2members_chat_room, delete_room, delete_user
from sNeeds.apps.videochats.tasks import create_room_with_users_in_skyroom, delete_room_and_users


def post_save_room_receiver(sender, instance, created, *args, **kwargs):
    if created:
        instance.sold_time_slot.used = True
        instance.sold_time_slot.save()

        create_room_with_users_in_skyroom.delay(instance.id)


def post_delete_room_receiver(sender, instance, *args, **kwargs):
    delete_room_and_users.delay(
        instance.user_id, instance.consultant_id, instance.room_id
    )


post_save.connect(post_save_room_receiver, sender=Room)
post_delete.connect(post_delete_room_receiver, sender=Room)
