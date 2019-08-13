from sNeeds.utils import skyroom
import random

NUMBER_OF_TRIES = 5
s = skyroom.SkyroomAPI()


def get_all_users():
    for i in range(0, NUMBER_OF_TRIES):
        response = s.getUsers()
        if response.get('ok'):
            break
        if i == NUMBER_OF_TRIES - 1:
            raise Exception("1")

    all_users = response.get("result")
    return all_users


def check_user_in_all_users(username, all_users):
    for user_dict in all_users:
        if username == user_dict.get("username"):
            return True
    return False


def get_user_id_in_all_users(username, all_users):
    for user_dict in all_users:
        if username == user_dict.get("username"):
            return user_dict.get("id")
    return None


def create_user_or_get_current_id(username, password, nickname):
    params = {
        "username": username,
        "password": password,
        "nickname": nickname,
        "status": 1,
        "is_public": True
    }
    all_users = get_all_users()

    if not check_user_in_all_users(username, all_users):

        for i in range(0, NUMBER_OF_TRIES):
            response = s.createUser(params=params)
            if response.get('ok'):
                break
            if i == NUMBER_OF_TRIES - 1:
                raise Exception("1")

        user_id = response.get("result")

    else:
        user_id = get_user_id_in_all_users(username, all_users)

    return user_id


def get_all_rooms():
    for i in range(0, NUMBER_OF_TRIES):
        response = s.getRooms()
        if response.get('ok'):
            break
        if i == NUMBER_OF_TRIES - 1:
            raise Exception("1")

    all_rooms = response.get("result")
    return all_rooms


def check_room_in_all_rooms(room_title, all_rooms):
    for room_dict in all_rooms:
        if room_title == room_dict.get("title"):
            return True
    return False


def get_room_id_in_all_rooms(room_title, all_rooms):
    for room_dict in all_rooms:
        if room_title == room_dict.get("title"):
            return room_dict.get("id")
    return None


def create_room(room_id):
    name = "مشاوره اسنیدز {}".format(room_id)
    title = "مشاوره اسنیدز {}".format(room_id)

    params = {
        "name": name,
        "title": title,
        "guest_login": False,
        "op_login_first": False,
        "max_users": 3
    }

    all_rooms = get_all_rooms()

    if not check_room_in_all_rooms(title, all_rooms):
        for i in range(0, NUMBER_OF_TRIES):

            response = s.createRoom(params=params)
            if response.get('ok'):
                break
            if i == NUMBER_OF_TRIES - 1:
                raise Exception("1")
        room_id = response.get("result")
    else:
        room_id = get_room_id_in_all_rooms(title, all_rooms)

    return room_id


def get_user_all_rooms(user_id):
    params = {
        "user_id": user_id
    }
    for i in range(0, NUMBER_OF_TRIES):
        response = s.getUserRooms(params=params)
        if response.get('ok'):
            break
        if i == NUMBER_OF_TRIES - 1:
            raise Exception("1")

    return response.get("result")


def is_user_in_rooms(room_id, user_rooms):
    for room_dict in user_rooms:
        if room_id == room_dict.get("room_id"):
            return True
    return False


def remove_user_from_room(user_id, room_id):
    params = {
        "user_id": user_id,
        "rooms": [room_id, ]
    }

    for i in range(0, NUMBER_OF_TRIES):
        response = s.removeUserRooms(params=params)
        if response.get('ok'):
            break
        if i == NUMBER_OF_TRIES - 1:
            raise Exception("1")


def make_user_room_presentor(user_id, room_id):
    params = {
        "room_id": room_id,
        "users": [
            {"user_id": user_id, "access": 2}
        ]
    }

    user_all_rooms = get_user_all_rooms(user_id)

    if  is_user_in_rooms(room_id, user_all_rooms):
        remove_user_from_room(user_id, room_id)

    for i in range(0, NUMBER_OF_TRIES):
        response = s.addRoomUsers(params=params)
        if response.get('ok'):
            break
        if i == NUMBER_OF_TRIES - 1:
            raise Exception("1")

    print(response)
# {
#   "action": "getLoginUrl",
#   "params": {
#     "room_id": 1,
#     "user_id": 1,
#     "language": "fa",
#     "ttl": 300
#   }
# }
#
# def get_login_url(room_id, user_id):
