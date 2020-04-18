import datetime

from sNeeds.utils import skyroom
from sNeeds.apps.store.models import SoldTimeSlotSale
from sNeeds.settings.config.SkyroomConfig import ALL_SKYROOM_USERS_PASSWORD, NUMBER_OF_TRIES, ROOM_MAX_USERS, \
    BEFORE_AFTER_CLASS_TIME_MINUTES

from .exceptions import SkyroomConnectException
from .models import Room

s = skyroom.SkyroomAPI()


def _get_all_users():
    response = s.getUsers()
    if response.get('ok'):
        all_users = response.get("result")
        return all_users
    else:
        raise SkyroomConnectException("Error using Skyroom, error:", str(response))


def _check_user_in_all_users(username, all_users):
    for user_dict in all_users:
        if username == user_dict.get("username"):
            return True
    return False


def _get_user_id_in_all_users(username, all_users):
    for user_dict in all_users:
        if username == user_dict.get("username"):
            return user_dict.get("id")
    return None


def create_user_or_get_current_id(username, password, nickname, email, expiry_date=None):
    params = {
        "username": username,
        "password": password,
        "nickname": nickname,
        "email": email,
        "expiry_date": expiry_date,
        "status": 1,
        "is_public": False
    }

    response = s.createUser(params=params)

    if response.get("ok"):
        user_id = response.get("result")

    elif response.get("error_message") == "نام کاربری تکراری است":
        all_users = _get_all_users()
        user_id = _get_user_id_in_all_users(username, all_users)
    else:
        raise SkyroomConnectException("Error using Skyroom, error:", str(response))

    return user_id


def _get_all_rooms():
    for i in range(0, NUMBER_OF_TRIES):
        response = s.getRooms()
        if response.get('ok'):
            break
        if i == NUMBER_OF_TRIES - 1:
            raise SkyroomConnectException("Error using Skyroom, error:", str(response))

    all_rooms = response.get("result")
    return all_rooms


def _check_room_in_all_rooms(room_title, all_rooms):
    for room_dict in all_rooms:
        if room_title == room_dict.get("title"):
            return True
    return False


def _get_room_id_in_all_rooms(room_title, all_rooms):
    for room_dict in all_rooms:
        if room_title == room_dict.get("title"):
            return room_dict.get("id")
    return None


def create_room_or_get(room_id, max_users):
    name = "room{}".format(room_id)
    title = "room{}".format(room_id)

    sold_session = SoldTimeSlotSale.objects.get(id=room_id)
    room_session_duration = (sold_session.end_time - sold_session.start_time + datetime.timedelta(
        minutes=2 * BEFORE_AFTER_CLASS_TIME_MINUTES)).seconds // 60

    params = {
        "name": name,
        "title": title,
        "guest_login": False,
        "op_login_first": False,
        "max_users": max_users,
        "session_duration": room_session_duration
    }

    response = s.createRoom(params=params)

    if response.get('ok'):
        return response.get("result")
    elif response.get("error_message") == "اتاقی با همین نام وجود دارد. از نام دیگری استفاده نمایید.":
        all_rooms = _get_all_rooms()
        return _get_room_id_in_all_rooms(title, all_rooms)
    else:
        raise SkyroomConnectException("Error using Skyroom, error:", str(response))


def _get_user_all_rooms(user_id):
    params = {
        "user_id": user_id
    }
    for i in range(0, NUMBER_OF_TRIES):
        response = s.getUserRooms(params=params)
        if response.get('ok'):
            break
        if i == NUMBER_OF_TRIES - 1:
            print(user_id)
            raise SkyroomConnectException("Error using Skyroom, error:", str(response))

    return response.get("result")


def _is_user_in_rooms(room_id, user_rooms):
    for room_dict in user_rooms:
        if room_id == room_dict.get("room_id"):
            return True
    return False


def _remove_user_from_room(user_id, room_id):
    params = {
        "user_id": user_id,
        "rooms": [room_id, ]
    }

    for i in range(0, NUMBER_OF_TRIES):
        response = s.removeUserRooms(params=params)
        if response.get('ok'):
            break
        if i == NUMBER_OF_TRIES - 1:
            raise SkyroomConnectException("Error using Skyroom, error:", str(response))


def make_user_room_presentor(user_id, room_id):
    params = {
        "room_id": room_id,
        "users": [
            {"user_id": user_id, "access": 2}
        ]
    }

    user_all_rooms = _get_user_all_rooms(user_id)

    if _is_user_in_rooms(room_id, user_all_rooms):
        _remove_user_from_room(user_id, room_id)

    for i in range(0, NUMBER_OF_TRIES):
        response = s.addRoomUsers(params=params)
        if response.get('ok'):
            break
        if i == NUMBER_OF_TRIES - 1:
            raise SkyroomConnectException("Error using Skyroom, error:", str(response))


def get_login_url_without_password(user_id, room_id, ttl):
    params = {
        "user_id": user_id,
        "room_id": room_id,
        "language": "fa",
        "ttl": ttl
    }
    response = s.getLoginUrl(params=params)
    if response.get("ok"):
        return response.get("result")
    elif " مورد نظر پیدا نشد" in response.get("error_message"):
        raise SkyroomConnectException("Error while creating login link.")
    else:
        raise SkyroomConnectException("Error using Skyroom, error:", str(response))


def create_2members_chat_room(
        username1, nickname1, user1email, username2, nickname2, user2email, roomid):
    sold_time_slot = SoldTimeSlotSale.objects.get(id=roomid)
    login_link_ttl = (sold_time_slot.end_time - sold_time_slot.start_time + datetime.timedelta(
        minutes=2 * BEFORE_AFTER_CLASS_TIME_MINUTES)).seconds // 60
    login_link_ttl *= 60

    if nickname1 == "" or nickname1 is None:
        nickname1 = "کاربر"

    if nickname2 == "" or nickname2 is None:
        nickname2 = "مشاور"
    user1_id = create_user_or_get_current_id(username1, ALL_SKYROOM_USERS_PASSWORD, nickname1, user1email)
    user2_id = create_user_or_get_current_id(username2, ALL_SKYROOM_USERS_PASSWORD, nickname2, user2email)

    room_id = create_room_or_get(roomid, ROOM_MAX_USERS)

    print(user1_id)
    print(user2_id)

    make_user_room_presentor(user1_id, room_id)
    make_user_room_presentor(user2_id, room_id)

    user1_url = get_login_url_without_password(user1_id, room_id, login_link_ttl)
    user2_url = get_login_url_without_password(user2_id, room_id, login_link_ttl)

    return_dict = {
        "user1_id": user1_id,
        "user2_id": user2_id,
        "room_id": room_id,
        "user1_url": user1_url,
        "user2_url": user2_url,
    }

    return return_dict


def delete_room(room_id):
    params = {
        "room_id": room_id
    }

    response = s.deleteRoom(params=params)

    if response.get('ok'):
        return response.get('result')
    elif "مورد نظر پیدا نشد." in response.get("error_message"):
        return None
    else:
        raise SkyroomConnectException("Error using Skyroom, error:", str(response))


def delete_user(user_id):
    params = {
        "user_id": user_id
    }

    response = s.deleteUser(params=params)
    if response.get('ok'):
        return response.get('result')
    elif "مورد نظر پیدا نشد." in response.get("error_message"):
        return None
    else:
        raise SkyroomConnectException("Error using Skyroom, error:", str(response))
