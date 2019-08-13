from sNeeds.utils import skyroom

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
