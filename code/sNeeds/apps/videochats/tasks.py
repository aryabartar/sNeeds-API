from __future__ import absolute_import, unicode_literals

from django.utils import timezone

from celery import task, shared_task
from celery.utils.log import get_task_logger

from sNeeds.settings.config.SkyroomConfig import BEFORE_AFTER_CLASS_TIME_MINUTES
from sNeeds.apps.store.models import SoldTimeSlotSale
from sNeeds.apps.videochats.models import Room
from sNeeds.apps.videochats.utils import create_2members_chat_room

logger = get_task_logger(__name__)


@task()
def create_rooms_from_sold_time_slots():
    qs = SoldTimeSlotSale.objects.filter(
        start_time__lte=timezone.now() + timezone.timedelta(minutes=BEFORE_AFTER_CLASS_TIME_MINUTES),
        start_time__gte=timezone.now() - timezone.timedelta(minutes=BEFORE_AFTER_CLASS_TIME_MINUTES),
        used=False
    )

    for obj in qs:
        Room.objects.create(sold_time_slot=obj)

    qs.update(used=True)


@task()
def delete_used_rooms():
    qs = Room.objects.filter(
        sold_time_slot__end_time__lte=timezone.now() - timezone.timedelta(minutes=5)
    )
    qs.delete()


@shared_task
def create_room_with_users_in_skyroom(room_id):
    room = Room.objects.get(id=room_id)
    user = room.sold_time_slot.sold_to
    consultant_user = room.sold_time_slot.consultant.user
    sold_time_slot_id = room.sold_time_slot.id

    username1 = user.email.split("@")[0]
    username2 = consultant_user.email.split("@")[0]

    data = create_2members_chat_room(
        username1=username1,
        nickname1=user.first_name,
        user1email=user.email,
        username2=username2,
        nickname2=consultant_user.first_name,
        user2email=consultant_user.email,
        roomid=sold_time_slot_id
    )

    room.room_id = data['room_id']

    room.user_id = data['user1_id']
    room.consultant_id = data['user2_id']

    room.user_login_url = data['user1_url']
    room.consultant_login_url = data['user2_url']

    room.save()


@shared_task
def delete_room(room_id):
    from sNeeds.apps.videochats.utils import delete_room
    delete_room(room_id)
