from django.db.models.signals import post_save, post_delete, pre_save, m2m_changed

from sNeeds.apps.videochats.models import Room
from sNeeds.apps.videochats.utils import create_2members_chat_room, delete_room, delete_user


def post_save_room_receiver(sender, instance, created, *args, **kwargs):
    if created:
        user = instance.sold_time_slot.sold_to
        consultant_user = instance.sold_time_slot.consultant.user
        sold_time_slot_id = instance.sold_time_slot.id

        data = create_2members_chat_room(
            user.id,
            user.first_name,
            user.email,
            consultant_user.id,
            consultant_user.first_name,
            consultant_user.email,
            sold_time_slot_id
        )

        instance.room_id = data['room_id']

        instance.user_id = data['user1_id']
        instance.consultant_id = data['user2_id']

        instance.user_login_url = data['user1_url']
        instance.consultant_login_url = data['user2_url']

        instance.save()


def post_delete_room_receiver(sender, instance, *args, **kwargs):
    delete_user(instance.user_id)
    delete_user(instance.consultant_id)
    delete_room(instance.room_id)


post_save.connect(post_save_room_receiver, sender=Room)
post_delete.connect(post_delete_room_receiver, sender=Room)
