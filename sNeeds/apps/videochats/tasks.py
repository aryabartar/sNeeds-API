from __future__ import absolute_import, unicode_literals

from celery import task, shared_task
from celery.utils.log import get_task_logger

from django.utils import timezone

from sNeeds.apps.store.models import SoldTimeSlotSale
from sNeeds.apps.videochats.models import Room
from sNeeds.apps.videochats.utils import create_2members_chat_room, delete_room, delete_user

logger = get_task_logger(__name__)


@task()
def create_rooms_from_sold_time_slots():
    qs = SoldTimeSlotSale.objects.filter(
        start_time__lte=timezone.now() + timezone.timedelta(minutes=5),
        start_time__gte=timezone.now(),
        used=False
    )

    for obj in qs:
        Room.objects.create(sold_time_slot=obj)

    qs.update(used=True)


@shared_task
def create_room_with_users_in_skyroom(room_id):
    room = Room.objects.get(id=room_id)
    user = room.sold_time_slot.sold_to
    consultant_user = room.sold_time_slot.consultant.user
    sold_time_slot_id = room.sold_time_slot.id

    data = create_2members_chat_room(
        user.id,
        user.first_name,
        user.email,
        consultant_user.id,
        consultant_user.first_name,
        consultant_user.email,
        sold_time_slot_id
    )

    room.room_id = data['room_id']

    room.user_id = data['user1_id']
    room.consultant_id = data['user2_id']

    room.user_login_url = data['user1_url']
    room.consultant_login_url = data['user2_url']

    room.save()


@shared_task
def delete_room_and_users(user_id, consultant_id, room_id):
    delete_user(user_id)
    delete_user(consultant_id)
    delete_room(room_id)
