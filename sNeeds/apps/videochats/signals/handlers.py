from django.db.models.signals import post_save, pre_delete, pre_save, m2m_changed

from sNeeds.apps.videochats.models import Room
from sNeeds.apps.videochats.utils import create_2members_chat_room


def post_save_room_receiver(sender, instance, created, *args, **kwargs):
    if created:
        user = instance.sold_time_slot.sold_to
        consultant_user = instance.sold_time_slot.consultant.user
        sold_time_slot_id = instance.sold_time_slot.id

        user_login_url, consultant_login_url = create_2members_chat_room(
            user.id,
            user.first_name,
            user.email,
            consultant_user.id,
            consultant_user.first_name,
            consultant_user.email,
            sold_time_slot_id
        )

        instance.user_login_url = user_login_url
        instance.consultant_login_url = consultant_login_url
        instance.save()


post_save.connect(post_save_room_receiver, sender=Room)
